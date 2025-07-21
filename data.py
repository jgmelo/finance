from datetime import datetime

crypto_reference_jvm = {
    'REF_001    ': {'Data'    : datetime.strptime("2025-01-02 18:52:03", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 120125.0                                                     ,
                   }                                                                         ,
    'REF_002    ': {'Data'    : datetime.strptime("2025-01-26 11:34:37", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 124862.0                                                     ,
                   }                                                                         ,
    'REF_003    ': {'Data'    : datetime.strptime("2025-02-16 20:40:59", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 128552.0                                                     ,
                   }                                                                         ,
    'REF_004    ': {'Data'    : datetime.strptime("2025-02-23 19:45:34", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 127128.0                                                     ,
                   }                                                                         ,
    'REF_005    ': {'Data'    : datetime.strptime("2025-03-30 20:03:08", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 131902.0                                                     ,
                   }     
}

crypto_jvm = {
    'COMPRA_001': {'Data'     : datetime.strptime("2025-01-02 18:52:03", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.00165647                                                   ,
                   'Preço BTC': 603693.4                                                     ,
                   }                                                                         ,
    'COMPRA_002': {'Data'     : datetime.strptime("2025-01-26 11:34:37", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.00159955                                                   ,
                   'Preço BTC': 625175.8                                                     ,
                   }                                                                         ,
    'COMPRA_003': {'Data'     : datetime.strptime("2025-02-16 20:40:59", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.00179745                                                   ,
                   'Preço BTC': 556343.7                                                     ,
                   }                                                                         ,
    'COMPRA_004': {'Data'     : datetime.strptime("2025-02-23 19:45:34", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.00180312                                                   ,
                   'Preço BTC': 554594.3                                                     ,
                   }                                                                         ,
    'COMPRA_005': {'Data'     : datetime.strptime("2025-03-30 20:03:08", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.00208031                                                   ,
                   'Preço BTC': 480698.0                                                     ,
                   }                                                                         ,
}

crypto_reference_sim = {
    'REF_001    ': {'Data'    : datetime.strptime("2025-02-20 19:45:31", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 120125.0                                                     ,
                   }                                                                         ,
    'REF_002    ': {'Data'    : datetime.strptime("2025-02-21 19:45:32", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 124862.0                                                     ,
                   }                                                                         ,
    'REF_003    ': {'Data'    : datetime.strptime("2025-02-22 19:45:33", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 128552.0                                                     ,
                   }                                                                         ,
    'REF_004    ': {'Data'    : datetime.strptime("2025-02-23 19:45:34", "%Y-%m-%d %H:%M:%S"),
                   'CDI'      : 1.01                                                         ,
                   'B3'       : 127128.0                                                     ,
                   }                                                                         ,
}

crypto_sim = {
    'COMPRA_001': {'Data'     : datetime.strptime("2025-02-20 19:45:31", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.06518479                                                   , # ETH
                   'Preço BTC': 15340.0                                                      ,
                   }                                                                         ,
    'COMPRA_002': {'Data'     : datetime.strptime("2025-02-21 19:45:32", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 0.24177949709                                                ,
                   'Preço BTC': 4136.0                                                       , # Cardano
                   }                                                                         ,
    'COMPRA_003': {'Data'     : datetime.strptime("2025-02-22 19:45:33", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 1.13895216401                                                , # SOL
                   'Preço BTC': 878.0                                                        ,
                   }                                                                         ,
    'COMPRA_004': {'Data'     : datetime.strptime("2025-02-23 19:45:34", "%Y-%m-%d %H:%M:%S"),
                   'Reais'    : 1000.0                                                       ,
                   'Bitcoin'  : 1.414427157                                                  , # Lite
                   'Preço BTC': 707.0                                                        ,
                   }                                                                         ,
}