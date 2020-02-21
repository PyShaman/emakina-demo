import security.zap as security


class TestVulnerabilities:
    zap = security.Zap()
    zap.start_zap()
    print("Checking connection to localhost")
    zap.check_zap_connection()
    print("connected to localhost")

    @staticmethod
    def test_flanders_nl_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://dienstencheques.vlaanderen.be/")

    @staticmethod
    def test_wallonie_fr_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://titres-services.wallonie.be/")

    @staticmethod
    def test_shutdown_zap():
        zap = security.Zap()
        zap.stop_zap()
