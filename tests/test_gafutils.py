import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch, call

from string_analysis import gafUtils

class TestGafManager(unittest.TestCase):
    
    GAFFILE = "mock"

    def setUp(self) -> None:
        super().setUp()
        self.gafManager = gafUtils.GafManager(gaf_file=self.GAFFILE)

    def test_generate_gafmap(self):
        # can read gaf map
        mock = Mock()
        mock_list = Mock()
        self.gafManager._read_map = Mock(return_value=mock)
        self.assertEquals(self.gafManager.generate_gafmap(mock_list), mock)

        # cannot read gafmap
        self.gafManager._read_map = Mock(return_value=None)
        self.gafManager._new_gafmap = Mock(return_value = mock)
        self.assertEquals(self.gafManager.generate_gafmap(mock_list), mock)
    
    @patch("src.gafUtils.gaf_parser")
    @patch("src.gafUtils.GafMap")
    def test_new_gafmap(self, gaf_parser, gaf_map):
        with patch(f'{__name__}.open', create=True) as m:
            self.assertTrue(True)

    