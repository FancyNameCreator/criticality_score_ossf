import os
from abc import ABC, abstractmethod
import pandas as pd
# from neo4j import GraphDatabase


DEPS_DATA_DIR_BASE_PATH = "C:\\DATA\\STUDIA\\Master\\P3\\ASE\\criticality_score_ossf\\criticality_score\\data"


class DependencyPagerankFetcher(ABC):
    @abstractmethod
    def try_get_dependency_pagerank_for_package(self, package_name, package_manager):
        pass

    @abstractmethod
    def get_all_packages(self, package_manager):
        pass

    @abstractmethod
    def get_all_package_managers(self):
        pass


# class Neo4jDependencyPagerankFetcher(DependencyPagerankFetcher):
#     def __init__(self):
#         self._uri = "neo4j://localhost:7687"
#         self._driver = GraphDatabase.driver(self._uri, auth=("neo4j", "password"))
#
#     @staticmethod
#     def _fetch_pagerank(tx, package_name, package_manager):
#         query = f"""MATCH (n:{package_manager})
#         WHERE n.PKG_NAME = "{package_name}"
#         RETURN n.PAGE_RANK;"""
#         result = tx.run(query)
#
#         return result.value()[0]
#
#     @staticmethod
#     def _fetch_all_packages(tx, package_manager):
#         query = f"""MATCH (n:{package_manager})
#             RETURN n.PKG_NAME;"""
#         result = tx.run(query)
#
#         return result.value()[0]
#
#     @staticmethod
#     def _fetch_all_package_managers(tx):
#         query = f"""MATCH (n) RETURN distinct labels(n);"""
#         result = tx.run(query)
#
#         return result.value()[0]
#
#     def try_get_dependency_pagerank_for_package(self, package_name, package_manager):
#         with self._driver.session() as session:
#             rank = session.execute_read(self._fetch_pagerank, package_name, package_manager)
#             if rank is None:
#                 raise PageRankNotAvailableException("Pagerank not available for this package")
#             else:
#                 return rank
#
#     def get_all_packages(self, package_manager):
#         # TODO: Fix me
#         pass
#
#     def get_all_package_managers(self):
#         # TODO: Fix me
#         pass


class CsvDependencyPagerankFetcher(DependencyPagerankFetcher):
    PKG_MANAGERS_LIST = [
        "alire",
        "cargo",
        "chromebrew",
        "clojars",
        "conan",
        "fpm",
        "homebrew",
        "luarocks",
        "nimble",
        "npm",
        # "ports",
        "rubygems",
        "vcpkg"
    ]

    def __init__(self):
        self._base_directory = DEPS_DATA_DIR_BASE_PATH

    def _load_dataframe(self, package_manager):
        path = os.path.join(self._base_directory, f"nodes_{package_manager.lower()}.csv")
        df = pd.read_csv(filepath_or_buffer=path, usecols=["PKG_NAME", "PAGE_RANK"])

        return df.applymap(lambda s: s.lower() if type(s) == str else s)

    def try_get_dependency_pagerank_for_package(self, package_name, package_manager):
        df = self._load_dataframe(package_manager)
        df_package_name = df.loc[df['PKG_NAME'] == package_name]

        return df_package_name.iloc[0]["PAGE_RANK"]

    def get_all_packages(self, package_manager):
        return self._load_dataframe(package_manager)['PKG_NAME'].tolist()

    def get_all_package_managers(self):
        return self.PKG_MANAGERS_LIST


class PageRankNotAvailableException(Exception):
    pass