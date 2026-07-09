import requests


class FCFProvider:

    STANDINGS_URL = (
        "https://egol.fcf.com.br/sisgol/"
        "Derw0757_TABELA_POR_FASEB.asp"
        "?SelStart1=2026"
        "&SelStop1=2026"
        "&SelStart2=698"
        "&SelStop2=698"
        "&Index=2"
        "&RunReport=Executar+relat%F3rio"
    )

    MATCHES_URL = (
        "https://egol.fcf.com.br/sisgol/"
        "DERW700B.asp"
        "?SelStart1=2026"
        "&SelStop1=2026"
        "&SelStart2=698"
        "&SelStop2=698"
        "&RunReport=Run+Report"
    )

    @staticmethod
    def get_standings_html() -> str:
        response = requests.get(
            FCFProvider.STANDINGS_URL,
            timeout=30,
        )

        response.raise_for_status()

        return response.text

    @staticmethod
    def get_matches_html() -> str:
        response = requests.get(
            FCFProvider.MATCHES_URL,
            timeout=30,
        )

        response.raise_for_status()

        return response.text