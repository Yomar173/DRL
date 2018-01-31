# DB Config. Info.

pg_config = {
    'user' : 'ckemnycsifpkiz',
    'passwd' : '4d12036347251f69345d5d8ee29ead50a562531208c8787e3c18807a1b287c06',
    'dbname' : 'dd1qfrfjh27kep',
    'host' : 'ec2-107-20-204-179.compute-1.amazonaws.com',
    'port' : '5432'
}


#amazonaws
"""
pg_config = {
    'user' : 'drlusr',
    'passwd' : 'DRL_BACKEND',
    'dbname' : 'drldb',
    'host' : 'awsdb.cg3h25ljtqea.us-east-2.rds.amazonaws.com',
    'port' : '5432'
}
"""
"""
pg_config = {
    'user' : 'drlusr',
    'passwd' : 'usr1',
    'dbname' : 'drldb'
}
"""

url_conn = "dbname=%s user=%s password=%s port=%s host=%s" % \
    (pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['port'], pg_config['host'])

"""
url_conn = "dbname=%s user=%s password=%s" % \
    (pg_config['dbname'], pg_config['user'], pg_config['passwd'])
"""