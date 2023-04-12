MATCH 
(m:ns1__music)<-[]-(b:ns1__Album),
(b)<-[]-(c) WHERE c:ns1__Artiste OR c:ns1__Auteur
RETURN m.ns1__songname, c.ns1__Nom;