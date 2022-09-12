from neo4j import GraphDatabase


class DependencyPagerankFetcher:
    def __init__(self):
        self._uri = "neo4j://localhost:7687"
        self._driver = GraphDatabase.driver(self._uri, auth=("neo4j", "6P87!xHs9f!CckgS"))

    def _fetch_pagerank(self, tx, name, platform):
        query = f"""MATCH (n:{platform})
        WHERE n.Name = "{name}"
        RETURN n.pagerank;"""
        result = tx.run(query)

        return result.value()[0]

    def get_dependency_pagerank(self, name, platform):
        with self._driver.session() as session:
            return session.execute_read(self._fetch_pagerank, name, platform)


if __name__ == '__main__':
    fetcher = DependencyPagerankFetcher()
    print(fetcher.get_dependency_pagerank("HardMock", "NuGet"))