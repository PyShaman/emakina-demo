from axe_selenium_python import Axe


class AxeEngine:

    def __init__(self):
        pass

    @staticmethod
    def inject_all_rules(driver, timestamp, culture, file_name, site):
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        f = open(f"results/{timestamp}_all/{culture}/" + file_name.replace("/", "_"), "w", encoding="utf-8")
        f.write(site + "\n")
        f.write(axe.report(results["violations"]))

    @staticmethod
    def inject_only_wcag(driver, timestamp, culture, file_name, site):
        options = """
        {
        runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa']
            }
        }"""
        axe = Axe(driver)
        axe.inject()
        results = axe.run(context=None, options=options)
        f = open(f"results/{timestamp}_wcag/{culture}/" + file_name.replace("/", "_"), "w", encoding="utf-8")
        f.write(site + "\n")
        f.write(axe.report(results["violations"]))
