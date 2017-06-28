#!/usr/bin/env python3

from pprint import pprint
import requests
import jinja2

template = '''
  protocols {
    BGP {
  {%- for lan in lans -%}  
    GROUP PEERSv4 {
     NEIGHBOURS {{lan.ipaddr4}} {
        DESCRIPTION {{net.name}};
        LOCAL-DETAILS {{lan.name}} {{lan.asn}}-{{lan.ix_id}};
        PEER-AS {{lan.asn}};
                            }
                }
    GROUP PEERSv6 {
     NEIGHBOURS {{lan.ipaddr6}} {
        DESCRIPTION {{net.name}};
        LOCAL-DETAILS {{lan.name}} {{lan.asn}}-{{lan.ix_id}};
        PEER-AS {{lan.asn}};
                            }
                }    
  {%- endfor -%}  
        }
            }                         
'''

def pdb_query(asn):

    r = requests.get("https://www.peeringdb.com/api/net?asn={}&depth=2".format(asn))
    return r.json()['data'][0]

def main():

    data = pdb_query(32934)

    t = jinja2.Template(template)

    a = 0
    Lans=[]

    while a < len(data['netixlan_set']):
        if data['netixlan_set'][a]['ix_id'] == 13:
            Lans.append(data['netixlan_set'][a])
            a = a+1
        else:
            a = a+1

    out = t.render(net=data, lans=Lans)
    pprint(out)

main()




