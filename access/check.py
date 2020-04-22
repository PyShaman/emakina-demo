from axe_selenium_python import Axe


class AxeEngine:

    def __init__(self):
        pass

    @staticmethod
    def inject_all_rules(driver, timestamp, culture, file_name, site):
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        fi = f"results/{timestamp}_all/{culture}/" + file_name.replace("/", "_")
        axe.write_results(results, fi)
        # f = open(f"results/{timestamp}_all/{culture}/" + file_name.replace("/", "_"), "w", encoding="utf-8")
        # f.write(site + "\n")
        # f.write(axe.report())
        # f.close()

    @staticmethod
    def inject_only_wcag2a(driver, timestamp, culture, file_name, site):
        options = """
        {
        runOnly: {
            type: 'tag',
            values: ['wcag2a']
            }
        }"""
        axe = Axe(driver)
        axe.inject()
        results = axe.run(context=None, options=options)
        f = open(f"results/{timestamp}_wcag2a/{culture}/" + file_name.replace("/", "_"), "w", encoding="utf-8")
        f.write(site + "\n")
        f.write(axe.report(results["violations"]))
        f.close()

    @staticmethod
    def inject_only_wcag2aa(driver, timestamp, culture, file_name, site):
        options = """
            {
            runOnly: {
                type: 'tag',
                values: ['wcag2aa','wcag2a']
                }
            }"""
        axe = Axe(driver)
        axe.inject()
        results = axe.run(context=None, options=options)
        f = open(f"results/{timestamp}_wcag2aa/{culture}/" + file_name.replace("/", "_"), "w", encoding="utf-8")
        f.write(site + "\n")
        f.write(axe.report(results["violations"]))
        f.close()
