from django.shortcuts import render
from rdflib import Graph,Namespace
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
# Create your views here.
def test(request):
    g = Graph()
    g.parse('http://dbpedia.org/resource/Pinocchio')
    dbo = Namespace("http://dbpedia.org/ontology/")
    
    print(type(g))
    # for s, p, o in g:
    #     print(s, p, o)
    temp = g.triples((None,dbo['creator'],None))
    print(type(temp))
    hasil = []
    for s,p,o in temp:
        print(s,p,o)
        hasil += ((s,p,o))
    response = {'isi' :hasil}
    return render(request, 'rdf.html',response)

def query(request):
    if(request.method=="POST"):
        try:
            sparql = SPARQLWrapper(
            "https://dbpedia.org/sparql"
            )
            sparql.setReturnFormat(JSON)
            query = request.POST["query"]
            sparql.setQuery("""
                PREFIX dbo: <http://dbpedia.org/ontology/>
                """ + query
            )
            ret = sparql.queryAndConvert()
            hasil = []
            for r in ret["results"]["bindings"]:
                print(r)
                hasil.append(r)

            response = {'isi':hasil,
                        "error":""}
        except Exception as e:
            
            print((str(e)[str(e).find("Response:")+9:]).replace("\\n","\n").replace("\\r","\r"))
            response = {"error":str(e)[str(e).find("Response:")+11:].replace("\\n","\n").replace("\\r","\r")}
    else :
        response = {"error":""}
    return render(request,'sparql.html',response)

def test_query(request):
    g = Graph(bind_namespaces="rdflib")
    dbo = Namespace("http://dbpedia.org/ontology/")
    g.bind("dbo",dbo)
    
    # q = prepareQuery(
    #     ,
    #     initNS={"dbo":dbo}
    # )
    qres =  g.query(
    """
    SELECT *
    WHERE {
      SERVICE <https://dbpedia.org/sparql> {
        ?s rdfs:label 'Pinocchio'@en ;
        dbo:creator ?o.
      }
    }
    LIMIT 3
    """
)
    hasil = []
    for row in qres:
        print(row.s)
        print(row.o)
    # for s,p,o in qres:
    #     print(s,p,o)
    #     hasil += (s,p,o)

    response = {'isi':hasil}
    return render(request,'rdf.html',response)

def blazegraph(request):
    g = Graph(bind_namespaces="rdflib")
    lokal = Namespace("http://knowledge.com/data#")
    g.bind("lokal",lokal)
    
    # q = prepareQuery(
    #     ,
    #     initNS={"dbo":dbo}
    # )
    qres =  g.query(
    """
    SELECT *
    WHERE {
      SERVICE <http://localhost:8000/blazegraph/namespace/kb/sparql> {
        ?s ?p ?o .
        
      }
    }
    ORDER BY ?s
    Limit 1
    
    """
)
    
    
    print(qres)
    hasil = []
    for row in qres:
        print(row.s,row.p,row.o)
        print(str(row.s),str(row.p),str(row.o))
        hasil+= [str(row.p),str(row.o)]
    # for s,p,o in qres:
    #     print(s,p,o)
    #     hasil += (s,p,o)

    response = {'isi':hasil}
    return render(request,'rdf.html',response)
