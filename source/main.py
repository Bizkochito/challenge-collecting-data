from typing import List

def extract_one_page(immo_url: str) -> dict:
    dict_of_informations_on_house = ...
    return dict_of_informations_on_house

def extract_x_urls(number_of_urls: int) -> List[str]:
    max 9990 urls
    return list_of_x_urls

def extract_all_data(list_of_urls: List[dict]) -> List[dict]:
    urls_list = extract_urls_list(immo_main_url)
    list_of_dicts = map(extract_one_page, urls_list)
    return list_of_dicts

start = time.perf_counter()
start_full = time.perf_counter()
list_of_urls = extract_x_urls(10000)

end = time.perf_counter()
execution_time = round((end - start), 2)
print(f'extract_x_urls took {execution_time} sec')


start = time.perf_counter()

data_list_of_dicts = extract_all_data(list_of_urls)

end = time.perf_counter()
execution_time = round((end - start), 2)
print(f'extract_all_data took {execution_time} sec')
end_full = time.perf_counter()
full_execution_time = round((end_full - start_full),2)
print(f'Full scraping too {full_execution_time} sec, or about ', full_execution_time/60, 'minutes.')