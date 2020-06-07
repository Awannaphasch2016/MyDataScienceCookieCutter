import datetime
import json
from typing import Dict
from typing import Optional

import numpy as np # type: ignore
import requests

from Utilities import my_timer
from Utilities.control_limit import ControlLimit
from Utilities.declared_typing import Json
from Utilities.declared_typing import PerDayAverage
from Utilities.declared_typing import RunningConstraints
from Utilities.declared_typing import SavedData
from Utilities.declared_typing import SubredditCollection
from Utilities.declared_typing import Url
from Utilities.test_conditions import \
    _check_that_all_selected_fields_are_returns


class RedditCrawler:
    def __init__(self,
                 subreddits_collection_class: SubredditCollection,
                 respond_type: str,
                 search_type: str,
                 verbose: int):

        self.verbose = verbose
        self.prepare_crawler(subreddits_collection_class, respond_type,
                             search_type)

    def prepare_crawler(self,
                        subreddits_collection_class: SubredditCollection,
                        respond_type: str,
                        search_type: str) -> None:

        self.respond_type = respond_type
        self.search_type = search_type

        if self.respond_type == 'avg':
            self.per_day_average: PerDayAverage
            self.per_day_average = {}
        elif self.respond_type == 'data':
            self.saved_data: SavedData
            self.saved_data = {}
        else:
            raise ValueError('respond_type must be avg or data')
        self.collection_name = subreddits_collection_class['name']
        self.collection = subreddits_collection_class['collection']

    def prepare_running_crawler(self,
                                before: Optional[int],
                                after: int) -> RunningConstraints:

        common_fields = 'author, author_flair_richtext, author_flair_type, ' \
                        'author_fullname,id, created_utc, permalink, retrieved_on, score, ' \
                        'subreddit, subreddit_id, total_awards_received, stickied, all_awardings'

        subreddit_fields = " domain, full_link, is_original_content, is_self, num_comments, pinned, selftext, subreddit_subscribers, title, upvote_ratio"

        comment_fields = 'body,parent_id,link_id'

        replace_and_split = lambda x: x.replace(' ', '').split(',')
        fields = replace_and_split(common_fields) + replace_and_split(
            subreddit_fields) + replace_and_split(comment_fields)
        fields = ','.join(fields)

        running_constraints: RunningConstraints
        running_constraints = {
            'before': before,
            'after': after,
            'aggs': 'created_utc',
            'frequency': 'day',
            'size': 1000,
            'metadata': 'true',
            'sort': 'asc',
            'fields': fields,
        }
        self.current_condition_str = f'collection_name = {self.collection_name} || search_type = {self.search_type} ||' \
                                     f' respond_type = {self.respond_type}|| {after} <= x < {before} '

        return running_constraints

    def make_request(self, running_constraints: RunningConstraints) -> Url:
        aggs = running_constraints['aggs']
        frequency = running_constraints['frequency']
        before = running_constraints['before']
        after = running_constraints['after']
        size = running_constraints['size']
        metadata = running_constraints['metadata']
        sort = running_constraints['sort']
        fields = running_constraints['fields']

        all_subreddit: str = ','.join(self.collection)
        endpoint_url = f'https://api.pushshift.io/reddit/search/{self.search_type}/?subreddit={all_subreddit}&' \
                       f'after={after}d&' \
                       f'size={size}&' \
                       f'metadata={metadata}&' \
                       f'sort={sort}&' \
                       f'fields={fields}&' \
                       f'aggs={aggs}&' \
                       f'frequency={frequency}'

        if before is not None:
            endpoint_url += f'&before={before}d'

        if self.collection_name != 'corona_states_with_tag':
            endpoint_url += f'&q=corona|covid|sarscov2'

        return endpoint_url

    @my_timer
    # @signature_logger
    def get_responds(self,
                     endpoint_url: str,
                     running_constraints: RunningConstraints) -> Json:

        def ensure_json(res):
            # TODO ERROR: json.loads(res.text) sometimes caused error at the first iteration (not sure why)
            if res.text is not None:
                res_text = res.text
                return json.loads(res_text)  # type = json
            else:
                return None

        def check_responds_consistency():
            if len(res['data']) > 0:
                for i in range(len(res['data'])):
                    _check_that_all_selected_fields_are_returns(
                        running_constraints,
                        res,
                        i,
                        self.current_condition_str,
                        self.verbose)
            else:
                # TODO create throwback exception to def run, so
                raise Warning('responds are empty')

        def check_responds_keys():
            keys = ['aggs', 'metadata', 'data']
            for i in keys:
                assert i in res, ''

        res = ensure_json(requests.get(endpoint_url))
        check_responds_consistency()
        check_responds_keys()

        return res

    @my_timer
    # @signature_logger
    def get_submission_avg_per_day(self,
                                   res: Json) -> float:

        def check_required_key():
            assert 'aggs' in res and 'data' in res, ''

        check_required_key()

        created_utc = res['aggs']['created_utc']
        num_days = len(created_utc)

        total = 0
        for ind, key in enumerate(created_utc):
            total += key['doc_count']

        avg = total / num_days

        if self.verbose:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(
                f' {self.current_condition_str} || avg_per_day given {num_days} days || {avg}')  # pass in variable to be pretty printed

        return avg

    def run(self,
            before: Optional[int],
            after: int) -> Dict[str, Dict]:

        control_limit = ControlLimit()
        try:
            responds_content = self.run_once(before, after)

            total_result = responds_content['metadata']['total_results']
            missing_results = 1000 - total_result
            missing_results = 0 if np.sign(missing_results) > 0 else missing_results
            if self.verbose:
                print(
                    f" {self.current_condition_str} || total_results = {total_result} || missing_result = {missing_results}")
            else:
                print(f'missing_reulst = {missing_results}')
        except Exception as e:
            if str(e) != 'responds are empty':
                raise NotImplementedError(f"exception occur in {self.run.__name__}")
            else:
                raise Warning(str(e))

        control_limit.control_pushshift_limit(total_number_of_request=1)

        return responds_content

    @my_timer
    # @signature_logger
    def run_once(self,
                 before: Optional[int],
                 after: int) -> Dict:

        running_constraints = self.prepare_running_crawler(before,
                                                           after)

        endpoint_url = self.make_request(running_constraints)
        res = self.get_responds(endpoint_url, running_constraints)
        reponds_content = self.apply_crawling_strategy(running_constraints, res)
        return reponds_content

    def adjust_after_step(self,
                          per_day_average: float,
                          max_responds_size: int) -> int:
        max_responds_threshold = max_responds_size - int(
            max_responds_size * 0.40)
        time_interval = int(max_responds_threshold / per_day_average)
        time_interval = 1 if time_interval < 1 else time_interval
        return time_interval

    def get_submission_data(self,
                            running_constraints: RunningConstraints,
                            res: Json) -> Dict:

        def get_meta_data() -> Dict:
            metadata = {}
            metadata['running_constraints'] = running_constraints

            keys = ['total_results', 'before', 'after', 'frequency',
                    'execution_time_milliseconds', 'sort', 'fields',
                    'subreddit']
            for key in keys:
                metadata[key] = res['metadata'][key]
            return metadata

        def get_data() -> Dict:
            data = res['data']
            return data

        def get_aggs() -> Dict:
            aggs = res['aggs']
            return aggs

        utc = res['data'][0]['created_utc']
        self.timestamp_utc = datetime.datetime.fromtimestamp(utc)

        self.saved_data['metadata'] = get_meta_data()
        self.saved_data['data'] = get_data()
        self.saved_data['aggs'] = get_aggs()

        def check_return_keys():
            assert 'metadata' in self.saved_data, ''
            assert 'data' in self.saved_data, ''
            assert 'aggs' in self.saved_data, ''

        check_return_keys()

        return self.saved_data
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(
        #     f' {self.current_condition_str} respond data => {self.per_day_average}')  # pass in variable to be pretty printedj

    def apply_crawling_strategy(self,
                                running_constraints: RunningConstraints,
                                res: Json) -> Dict:
        if self.respond_type == 'avg':
            raise DeprecationWarning(f'no longer support {self.respond_type}')

        elif self.respond_type == 'data':
            return self.get_submission_data(running_constraints,
                                            res)
        else:
            raise ValueError('')
