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
    'COMPRA_001': {'Data'      : datetime.strptime("2025-01-02 18:52:03", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00165647                                                   ,
                   'Preço'     : 603693.4                                                     ,
                   }                                                                          ,
    'COMPRA_002': {'Data'      : datetime.strptime("2025-01-26 11:34:37", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00159955                                                   ,
                   'Preço'     : 625175.8                                                     ,
                   }                                                                          ,
    'COMPRA_003': {'Data'      : datetime.strptime("2025-02-16 20:40:59", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00179745                                                   ,
                   'Preço'     : 556343.7                                                     ,
                   }                                                                          ,
    'COMPRA_004': {'Data'      : datetime.strptime("2025-02-23 19:45:34", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00180312                                                   ,
                   'Preço'     : 554594.3                                                     ,
                   }                                                                          ,
    'COMPRA_005': {'Data'      : datetime.strptime("2025-03-30 20:03:08", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00208031                                                   ,
                   'Preço'     : 480698.0                                                     ,
                   }                                                                          ,
    'COMPRA_006': {'Data'      : datetime.strptime("2025-07-14 15:28:20", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 2000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00296445                                                   ,
                   'Preço'     : 674661.4                                                     ,
                   }                                                                          ,
    'COMPRA_007': {'Data'      : datetime.strptime("2025-07-20 19:04:03", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00150249                                                   ,
                   'Preço'     : 665562.0                                                     ,
                   }                                                                          ,
    'COMPRA_008': {'Data'      : datetime.strptime("2025-10-20 17:17:28", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 1000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00166557                                                   ,
                   'Preço'     : 600395.0599494                                               ,
                   }                                                                          ,
    'COMPRA_009': {'Data'      : datetime.strptime("2025-10-20 17:39:44", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 3000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00499876                                                   ,
                   'Preço'     : 600148.8                                                     ,
                   }                                                                          ,
    'COMPRA_010': {'Data'      : datetime.strptime("2025-11-30 19:50:52", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 3000.0                                                       ,
                   'Cripto'    : 'Bitcoin'                                                    ,
                   'Quantidade': 0.00608303                                                   ,
                   'Preço'     : 493175.3                                                     ,
                   }                                                                          ,
    'COMPRA_011': {'Data'      : datetime.strptime("2026-01-15 14:00:00", "%Y-%m-%d %H:%M:%S"),
                   'Reais'     : 500.0                                                        ,
                   'Cripto'    : 'Ethereum'                                                   ,
                   'Quantidade': 0.025                                                        ,
                   'Preço'     : 20000.0                                                      ,
                   }                                                                          ,
}

crypto_sales = {
    'VENDA_001': {
        'Data'      : datetime.strptime("2025-03-30 12:00:00", "%Y-%m-%d %H:%M:%S"),
        'Reais'     : 800.0,
        'Cripto'    : 'Bitcoin',
        'Preço'     : 550000.0,
    },
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


def get_sale_info(purchase_id: str):
    """Retrieve sale information for a given purchase ID.

    Args:
        purchase_id: Identifier of the purchase (e.g., "COMPRA_001").

    Returns:
        A dictionary with sale details or None if the purchase ID was not sold.
    """

    return crypto_sales.get(purchase_id)

