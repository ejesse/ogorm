from tests import OgormTest
import logging


class TestModels(OgormTest):
    
    def test_create_a_basic_class(self):
        cluster_id = self.client.command( "create class my_class extends V" )
        r = self.client.command("insert into my_class ( 'accommodation', 'work', 'holiday' ) values( 'B&B', 'garage', 'mountain' )")
        
        