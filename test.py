from src.web2md import convert_url_to_markdown, convert_urls_to_markdown, async_convert_url_to_markdown, async_convert_urls_to_markdown
import asyncio
import timeit
import time


list_of_100_urls = [
  "http://www.youtube.com",
  "http://www.facebook.com",
  "http://www.baidu.com",
  "http://www.yahoo.com",
  "http://www.amazon.com",
  "http://www.wikipedia.org",
  "http://www.qq.com",
  "http://www.google.co.in",
  "http://www.twitter.com",
  "http://www.live.com",
  "http://www.taobao.com",
  "http://www.bing.com",
  "http://www.instagram.com",
  "http://www.weibo.com",
  "http://www.sina.com.cn",
  "http://www.linkedin.com",
  "http://www.yahoo.co.jp",
  "http://www.msn.com",
  "http://www.vk.com",
  "http://www.google.de",
  "http://www.yandex.ru",
  "http://www.hao123.com",
  "http://www.google.co.uk",
  "http://www.reddit.com",
  "http://www.ebay.com",
  "http://www.google.fr",
  "http://www.t.co",
  "http://www.tmall.com",
  "http://www.google.com.br",
  "http://www.360.cn",
  "http://www.sohu.com",
  "http://www.amazon.co.jp",
  "http://www.pinterest.com",
  "http://www.netflix.com",
  "http://www.google.it",
  "http://www.google.ru",
  "http://www.microsoft.com",
  "http://www.google.es",
  "http://www.wordpress.com",
  "http://www.gmw.cn",
  "http://www.tumblr.com",
  "http://www.paypal.com",
  "http://www.blogspot.com",
  "http://www.imgur.com",
  "http://www.stackoverflow.com",
  "http://www.aliexpress.com",
  "http://www.naver.com",
  "http://www.ok.ru",
  "http://www.apple.com",
  "http://www.github.com",
  "http://www.chinadaily.com.cn",
  "http://www.imdb.com",
  "http://www.google.co.kr",
  "http://www.fc2.com",
  "http://www.jd.com",
  "http://www.blogger.com",
  "http://www.163.com",
  "http://www.google.ca",
  "http://www.whatsapp.com",
  "http://www.amazon.in",
  "http://www.office.com",
  "http://www.tianya.cn",
  "http://www.google.co.id",
  "http://www.youku.com",
  "http://www.rakuten.co.jp",
  "http://www.craigslist.org",
  "http://www.amazon.de",
  "http://www.nicovideo.jp",
  "http://www.google.pl",
  "http://www.soso.com",
  "http://www.bilibili.com",
  "http://www.dropbox.com",
  "http://www.xinhuanet.com",
  "http://www.outbrain.com",
  "http://www.pixnet.net",
  "http://www.alibaba.com",
  "http://www.alipay.com",
  "http://www.microsoftonline.com",
  "http://www.booking.com",
  "http://www.googleusercontent.com",
  "http://www.google.com.au",
  "http://www.popads.net",
  "http://www.cntv.cn",
  "http://www.zhihu.com",
  "http://www.amazon.co.uk",
  "http://www.diply.com",
  "http://www.coccoc.com",
  "http://www.cnn.com",
  "http://www.bbc.co.uk",
  "http://www.twitch.tv",
  "http://www.wikia.com",
  "http://www.google.co.th",
  "http://www.go.com",
  "http://www.google.com.ph",
  "http://www.doubleclick.net",
  "http://www.onet.pl",
  "http://www.googleadservices.com",
  "http://www.accuweather.com",
  "http://www.googleweblight.com",
  "http://www.answers.yahoo.com",
]

async def time_async_function(func, *args, **kwargs):
    """
    Measure the execution time of an async function.

    Parameters:
        func (coroutine): The asynchronous function to be timed.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        tuple: (result, elapsed_time) where
            - result: The return value of the async function.
            - elapsed_time: Execution time in seconds.
    """
    start_time = time.monotonic()
    result = await func(*args, **kwargs)
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    return result, elapsed_time


async def main():


  # use timeit to time the conversion of the first 100 urls
  # elapsed_time = timeit.timeit(lambda: convert_urls_to_markdown(list_of_100_urls[:n]), number=1)

  # result, elapsed_time = await time_async_function(async_convert_urls_to_markdown, ["https://www.google.com"])



  result, elapsed_time_async = await time_async_function(async_convert_urls_to_markdown, list_of_100_urls)
  print("Took ", elapsed_time_async, " seconds")

  sorted_result = sorted(result, key=lambda x: x[1])

  for i, res in enumerate(sorted_result):
    print(f"{list_of_100_urls[i]} took {res[1]} seconds")


asyncio.run(main())






