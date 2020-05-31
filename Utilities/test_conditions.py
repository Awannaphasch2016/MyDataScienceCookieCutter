from typing import Dict
from typing import List

from Utilities.declared_typing import Json
from Utilities.declared_typing import RunningConditions
from Utilities.declared_typing import RunningConstraints


def check_running_conditions(running_conditions: RunningConditions) -> None:
    for i in ['respond_type', 'collection_name', 'crawler_option', 'search_type']:
        if i not in running_conditions:
            raise ValueError('')


        if running_conditions['collection_name'] not in  ['corona_general', 'corona_regions', 'corona_states_with_tag']:
            raise ValueError('collection_name are not availble')

        if running_conditions['crawler_option'] not in ['reddit', 'twitter']:
            raise ValueError('crawler_option are not availble')
        else:
            if running_conditions['search_type'] not in ['comment', 'submission']:
                raise ValueError('search_type are not abailble')

            if running_conditions['respond_type'] not in ['avg', 'data']:
                raise ValueError('respond_type are not availble')

def _check_that_all_selected_fields_are_returns(running_constraints: RunningConstraints,
                                                           res: Json,
                                                           ind: int,
                                                            current_condition_str: str,
                                                            verbose: int
                                                           ):
    before = running_constraints['before']
    after = running_constraints['after']
    fields = running_constraints['fields']

    current_condition_str_with_ind = current_condition_str + f" || ind = {ind} ||"
    res_data = res['data'][ind]
    len_res_data_key = len(list(res_data.keys()))
    num_fields = len(fields.split(','))

    if len_res_data_key != num_fields:
        def get_missing_keys():
            incorrect_fields = set(
                res_data.keys()).symmetric_difference(
                set(fields.split(',')))
            all_missing_keys = "[" + ','.join(
                list(incorrect_fields)) + "]"
            incorrect_fields_error = f'{current_condition_str_with_ind} ' \
                                     f'the following fields are incorrect {all_missing_keys} '
            return (list(incorrect_fields), all_missing_keys,
                    incorrect_fields_error)

        def add_missing_keys(incorrect_fields: List,
                             all_missing_keys: str,
                             incorrect_fields_error: str):
            if verbose:
                print(
                    f'{current_condition_str_with_ind}  adding keys = {all_missing_keys}')

            for missing_key in incorrect_fields:
                if missing_key not in res['data']:
                    res['data'][ind][missing_key] = None

            assert len(list(res['data'][0])) == num_fields, \
                get_missing_keys()[2]

        add_missing_keys(*get_missing_keys())

    else:
        print(
            f'{current_condition_str_with_ind} || all selected fields are retuned ')


