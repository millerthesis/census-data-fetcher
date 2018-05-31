from meta.config import read_default_api_key





if __name__ == '__main__':
    key = read_default_api_key()
    # tablecodes = get_acs_tablecodes()

    # print("tract urls:")
    # urls = batch_acs_urls('2016', tablecodes, 'tract', api_key=key)
    # for u in urls:
    #     print(u)
    # print("\n")

    # for g in ['county', 'state', 'us']:
    #     urls = batch_acs_urls('2016', tablecodes, g, api_key=key)
    #     print(urls[0])

