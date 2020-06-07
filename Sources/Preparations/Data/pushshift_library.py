import datetime
import pathlib
import time

from Sources.Preparations.Data.RedditCrawler import RedditCrawler
from Utilities import my_timer
from Utilities import save_to_file
from Utilities.declared_typing import RedditCralwerCondition
from Utilities.declared_typing import RunningConditions
from Utilities.declared_typing import SubredditCollection
from Utilities.test_conditions import check_running_conditions
from global_parameters import BASE_DIR


def get_saved_file_path(timestamp: datetime.datetime,
                        path_name: pathlib.Path) -> pathlib.Path:
    saved_file = pathlib.Path(
        path_name) / f'after_date={timestamp.date()}.pickle'
    return saved_file


def run_reddit_crawler(
        subreddit_collection_class: SubredditCollection,
        initial_day_interval: int,
        request_timestamp: str,
        respond_type: str,
        search_type: str
) -> None:
    try:
        time.strptime(request_timestamp, "%Y%m%d-%H%M%S")  # Test
    except:
        raise ValueError(
            f'time_stamp must have the following format %Y%m%d-%H%M%S')

    after = initial_day_interval
    before = None
    next_interval = None
    max_after = 100
    assert after <= max_after, 'after have to be less than max_after'

    while after <= max_after:
        reddit_crawler = RedditCrawler(subreddit_collection_class,
                                       respond_type=respond_type,
                                       search_type=search_type,
                                       verbose=False)

        interval = next_interval if next_interval is not None else after
        print(f" || day interval = {interval}")

        try:
            responds_content = reddit_crawler.run(before, after)

            per_day_average = reddit_crawler.get_submission_avg_per_day(
                responds_content)
            next_interval = reddit_crawler.adjust_after_step(per_day_average,
                                                             max_responds_size=1000)

            saved_file = get_saved_file_path(reddit_crawler.timestamp_utc,
                                             path_name=BASE_DIR / f'Outputs/Data/{reddit_crawler.collection_name}/{reddit_crawler.search_type}/{reddit_crawler.respond_type}')
            save_to_file(responds_content,
                         saved_file)
        except Exception as e:
            if str(e) != 'responds are empty':
                raise NotImplementedError(
                    f"unknown error occur in {run_reddit_crawler.__name__} ")
            else:
                print(str(e))
                next_interval = per_day_average  # reintialize next-interval to be last calculated per_day_average

        before = after + 1
        after = before + next_interval
        print()
    else:
        if after > max_after:
            print(
                f' || after > max_after({max_after}) || after is set to {max_after}')
            after = 100
        else:
            raise ValueError('')

        reddit_crawler = RedditCrawler(subreddit_collection_class,
                                       respond_type=respond_type,
                                       search_type=search_type,
                                       verbose=False)
        responds_content = reddit_crawler.run(before, after)

        saved_file = get_saved_file_path(reddit_crawler.timestamp_utc,
                                         path_name=BASE_DIR / f'Outputs/Data/{reddit_crawler.collection_name}/{reddit_crawler.search_type}/{reddit_crawler.respond_type}')
        save_to_file(responds_content,
                     saved_file)
        print(' >>>> finished crawling data <<<<')
        print()


def reddit_crawler_condition(
        running_conditions: RunningConditions) -> RedditCralwerCondition:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    General = ['Corona', 'COVID19', 'CoronavirusUS']
    Region = ['CoronavirusMidwest', 'CoronavirusSouth', 'CoronavirusSouthEast',
              'CoronavirusWest']

    # --------List of USA States
    states_subreddit = ['alabama', 'alaska', 'arizona', 'arkansas',
                        'california',
                        'colorado', 'connecticut', 'delaware', 'florida',
                        'georgia',
                        'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
                        'kansas', 'kentucky',
                        'louisiana', 'maine', 'maryland', 'massachusetts',
                        'michigan', 'minnesota', 'mississippi',
                        'missouri', 'montana', 'nebraska', 'nevada',
                        'newhampshire',
                        'newjersey', 'newmexico', 'newyork', 'northcarolina',
                        'northdakota', 'ohio',
                        'oklahoma', 'oregon', 'pennsylvania', 'rhodeisland',
                        'southcarolina', 'southdakota', 'tennessee', 'texas',
                        'utah', 'vermont', 'virginia',
                        'washington', 'westvirginia', 'wisconsin', 'wyoming']

    subreddit_collection_class: SubredditCollection
    initial_day_interval = 1

    if running_conditions['collection_name'] == 'corona_general':
        subreddit_collection_class = {'collection': General,
                                      'name': running_conditions[
                                          'collection_name']}

        crawler_condition: RedditCralwerCondition = {
            'subreddit_collection_class': subreddit_collection_class,
            'initial_day_interval': initial_day_interval,  # 9
            'request_timestamp': timestamp,
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type']
        }

    elif running_conditions['collection_name'] == 'corona_regions':
        subreddit_collection_class = {'collection': Region,
                                      'name': running_conditions[
                                          'collection_name']}

        crawler_condition: RedditCralwerCondition = {
            'subreddit_collection_class': subreddit_collection_class,
            'initial_day_interval': initial_day_interval,  # 100
            'request_timestamp': timestamp,
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type']
        }

    elif running_conditions['collection_name'] == 'corona_states_with_tag':
        subreddit_collection_class = {'collection': states_subreddit,
                                      'name': running_conditions[
                                          'collection_name']}

        crawler_condition: RedditCralwerCondition = {
            'subreddit_collection_class': subreddit_collection_class,
            'initial_day_interval': initial_day_interval,  # 8
            'request_timestamp': timestamp,
            'respond_type': running_conditions['respond_type'],
            'search_type': running_conditions['search_type']
        }

    else:
        raise ValueError('collection_name is not supported')

    return crawler_condition


def select_crawler_condition(
        running_conditions: RunningConditions) -> RedditCralwerCondition:
    if running_conditions['crawler_option'] == 'reddit':
        crawler_conditions = reddit_crawler_condition(running_conditions)
    elif running_conditions['crawler_option'] == 'twitter':
        raise NotImplementedError
    return crawler_conditions


@my_timer
def main() -> None:
    all_running_conditions = []
    one_running_conditions = {'crawler_option': 'reddit',
                              'collection_name': 'corona_general',
                              'respond_type': 'data',
                              'search_type': 'submission'
                              }
    two_running_conditions = {'crawler_option': 'reddit',
                              'collection_name': 'corona_regions',
                              'respond_type': 'data',
                              'search_type': 'submission'
                              }
    three_running_conditions = {'crawler_option': 'reddit',
                                'collection_name': 'corona_states_with_tag',
                                'respond_type': 'data',
                                'search_type': 'submission'
                                }
    four_running_conditions = {'crawler_option': 'reddit',
                               'collection_name': 'corona_general',
                               'respond_type': 'data',
                               'search_type': 'comment'
                               }
    five_running_conditions = {'crawler_option': 'reddit',
                               'collection_name': 'corona_regions',
                               'respond_type': 'data',
                               'search_type': 'comment'
                               }
    six_running_conditions = {'crawler_option': 'reddit',
                              'collection_name': 'corona_states_with_tag',
                              'respond_type': 'data',
                              'search_type': 'comment'
                              }

    # all_running_conditions.append(one_running_conditions)
    all_running_conditions.append(two_running_conditions)
    # all_running_conditions.append(three_running_conditions)

    # all_running_conditions.append(four_running_conditions)
    # all_running_conditions.append(five_running_conditions)
    # all_running_conditions.append(six_running_conditions)

    for running_conditions in all_running_conditions:
        check_running_conditions(running_conditions)
        crawler_condition = select_crawler_condition(
            running_conditions=running_conditions)
        run_reddit_crawler(**crawler_condition)

    # TODO
    #   : push to github (if not yet created branch and create one call dev_anak)
    #   :implement code for reddit comment
    #       : using the lat 20 days to deterimine amoung of day interval (do this)
    #   :write script to run program every day. (get new info everyday)
    #   at 9 pm
    #  :test the following cases
    #       >create class template that can used by twitter too


if __name__ == '__main__':
    main()
