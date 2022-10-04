from neo4j import GraphDatabase


class DependencyPagerankFetcher:
    def __init__(self):
        self._uri = "neo4j://localhost:7687"
        self._driver = GraphDatabase.driver(self._uri, auth=("neo4j", "password"))

    @staticmethod
    def _fetch_pagerank(tx, package_name, package_manager):
        query = f"""MATCH (n:{package_manager})
        WHERE n.PKG_NAME = "{package_name}"
        RETURN n.PAGE_RANK;"""
        result = tx.run(query)

        return result.value()[0]

    @staticmethod
    def _fetch_all_packages(tx, package_manager):
        query = f"""MATCH (n:{package_manager})
            RETURN n.PKG_NAME;"""
        result = tx.run(query)

        return result.value()[0]

    @staticmethod
    def _fetch_all_package_managers(tx):
        query = f"""MATCH (n) RETURN distinct labels(n);"""
        result = tx.run(query)

        return result.value()[0]

    def try_get_dependency_pagerank_for_package(self, package_name, package_manager):
        with self._driver.session() as session:
            rank = session.execute_read(self._fetch_pagerank, package_name, package_manager)
            if rank is None:
                raise PageRankNotAvailableException("Pagerank not available for this package")
            else:
                return rank

    @staticmethod
    def get_all_packages():
        # TODO: Fix me
        pass

    @staticmethod
    def get_all_package_managers():
        # TODO: Fix me
        pass


class PageRankNotAvailableException(Exception):
    pass