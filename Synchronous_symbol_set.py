''''
同步符号集
'''
#Analysis chart with synchronization mark
#-1 represents empty cell in the Analysis chart
#0 represents ξ in the Analysis chart
chart={"E id":"T E1","E1 id":-1,"T id":"F T1","T1 id":-1,"F id":"id",
       "E +":-1,"E1 +":"+ T E1","T +":"synch","T1 +":0,"F +":"synch",
       "E *":-1,"E1 *":-1,"T *":-1,"T1 *":"* F T1","F *":"synch",
       "E (":"T E1","E1 (":-1,"T (":"F T1","T1 (":-1,"F (":"( E )",
        "E )":"synch","E1 )":0,"T )":"synch","T1 )":0,"F )":"synch",
       "E #":"synch","E1 #":0,"T #":"synch","T1 #":0,"F #":"synch"
       }