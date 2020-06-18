HOST = 'https://alpha-jena-fusek.aidigger.com:443'
DATASET = 'xxx'
ENDPOINT = '{}/{}'.format(HOST, DATASET)
QUERY = ENDPOINT + '/query'
UPDATE = ENDPOINT + '/update'
GSP = ENDPOINT + '/data?default'

# properties and classes namespace
namespace = 'http://www.eigentech.ai#'

# SPARQL prefix
prefix = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <{}>
'''.format(namespace)