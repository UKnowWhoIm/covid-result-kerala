# Covid Result Kerala

View your COVID result as soon as it is published. Applicable only for tests in kerala.

## Prerequisites

- Python 3.4+
- Firefox and [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## Instructions

1. Clone this repo
2. Create a data.json file according to the format in `data.json.example`. For knowing your SRF_NO visit [link](https://labsys.health.kerala.gov.in/Download_report/know_my_SRF/).
3. Create venv and activate it.
4. Install dependancies by running `pip install -r requirements.txt`.
5. Run `python main.py`.
6. Keep the process running, if your result is available it will be popped up.

## License

This project is licensed under the permissive open-source [MIT license](LICENSE).
