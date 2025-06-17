import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 0.3,
    status_list: set = (500, 502, 503, 504),
    session: requests.Session = None,
) -> requests.Session:
    """
    Returns a requests session that will retry on certain HTTP status codes.

    Args:
        retries (int, optional): Number of times to retry the request. Defaults to 3.
        backoff_factor (float, optional): Factor to apply to the delay between retries.
            Defaults to 0.3.
        status_list (tuple, optional): List of HTTP status codes that should trigger a retry.
            Defaults to (500, 502, 504).
        session (requests.Session, optional): Existing requests session. Defaults to None.
    """
    session = session or requests.Session()
    retry_strategy = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_list,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


if __name__ == "__main__":
    test_url = "https://http.dev"  # Example URL for testing

    # usage example
    response = requests_retry_session().get(test_url)
    print(response.status_code)

    s = requests.Session()
    s.auth = ("user", "pass")
    s.headers.update({"x-test": "true"})

    response = requests_retry_session(session=s).get(test_url)

    # test example
    t0 = time.time()
    try:
        response = requests_retry_session().get(
            url="http://localhost:9999",
        )
    except Exception as x:
        print("It failed :(", x.__class__.__name__)
    else:
        print("It eventually worked", response.status_code)
    finally:
        t1 = time.time()
        print("Took", t1 - t0, "seconds")
