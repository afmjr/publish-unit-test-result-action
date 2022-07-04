import os
import pathlib
from typing import Iterable, Callable

from lxml import etree

from publish.junit import JUnitTreeOrException, ParsedJUnitFile

with (pathlib.Path(__file__).parent / 'xslt' / 'trx-to-junit.xslt').open('r', encoding='utf-8') as r:
    transform_trx_to_junit = etree.XSLT(etree.parse(r))


def parse_trx_files(files: Iterable[str],
                    progress: Callable[[ParsedJUnitFile], ParsedJUnitFile] = lambda x: x) -> Iterable[ParsedJUnitFile]:
    """Parses trx files."""
    def parse(path: str) -> JUnitTreeOrException:
        """Parses a trx file and returns either a JUnitTree or an Exception."""
        if not os.path.exists(path):
            return FileNotFoundError(f'File does not exist.')
        if os.stat(path).st_size == 0:
            return Exception(f'File is empty.')

        try:
            trx = etree.parse(path)
            return transform_trx_to_junit(trx)
        except BaseException as e:
            return e

    return [progress((result_file, parse(result_file))) for result_file in files]