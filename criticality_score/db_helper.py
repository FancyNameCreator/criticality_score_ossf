from neo4j import GraphDatabase

CONVERT_LANGUAGE_TO_PLATFORM = {
        "C": "",
        "C++": "",
        "C#": "NuGet",
        # "Go": "Go",                        # Dataset does not contain dependency relations for Go
        "Java": "Maven",
        "JavaScript": "NPM",
        "PHP": "Packagist",
        "Python": "Pypi",
        "Ruby": "Rubygems",
        "Scala": "Maven",                   # TODO: Check if that's correct
        "Typescript": "NPM"
    }


class DependencyPagerankFetcher:
    def __init__(self):
        self._uri = "neo4j://localhost:7687"
        self._driver = GraphDatabase.driver(self._uri, auth=("neo4j", "password"))

    @staticmethod
    def _fetch_pagerank(tx, package_name, package_manager):
        query = f"""MATCH (n:{package_manager})
        WHERE n.Name = "{package_name}"
        RETURN n.pagerank;"""
        result = tx.run(query)

        return result.value()[0]

    def try_get_dependency_pagerank(self, repo) -> float:
        if repo.language in CONVERT_LANGUAGE_TO_PLATFORM.keys():
            platform = CONVERT_LANGUAGE_TO_PLATFORM[repo.language]
        else:
            raise PageRankNotAvailableException

        with self._driver.session() as session:
            rank = session.execute_read(self._fetch_pagerank, repo.name, platform)
            if rank is None:
                raise PageRankNotAvailableException("Pagerank not available for this package")
            else:
                return rank

    def try_get_dependency_pagerank_for_package(self, package_name, package_manager):
        with self._driver.session() as session:
            rank = session.execute_read(self._fetch_pagerank, package_name, package_manager)
            if rank is None:
                raise PageRankNotAvailableException("Pagerank not available for this package")
            else:
                return rank

    def is_dependency_pagerank_available(self, repo) -> bool:
        if repo.language in CONVERT_LANGUAGE_TO_PLATFORM.keys():
            platform = CONVERT_LANGUAGE_TO_PLATFORM[repo.language]
        else:
            return False

        with self._driver.session() as session:
            rank = session.execute_read(self._fetch_pagerank, repo.name, platform)
            return rank is not None


class PageRankNotAvailableException(Exception):
    pass