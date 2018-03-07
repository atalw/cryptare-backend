import requests
import pyrebase
import json
config = {
    "apiKey": " AIzaSyBdlfUxRDXdsIXdKPFk-hBu_7s272gGE6E ",
    "authDomain": "atalwcryptare.firebaseapp.com",
    "databaseURL": "https://atalwcryptare.firebaseio.com/",
    "storageBucket": "atalwcryptare.appspot.com",
    "serviceAccount": "../service_account_info/Cryptare-9d04b184ba96.json"
}

firebase = pyrebase.initialize_app(config)

# # Get a reference to the auth service
# auth = firebase.auth()
#
# # Log the user in
# user = auth.sign_in_with_email_and_password(sys.argv[1], sys.argv[2])

# Get a reference to the database service
db = firebase.database()

# coins = ["BTC", "ETH", "LTC", "BCH", "XRP"]
# dict = {'AION': {'rank': 62.0, 'name': 'Aion'}, 'C20': {'rank': 161.0, 'name': 'CRYPTO20'}, 'TRIG': {'rank': 238.0, 'name': 'Triggers'}, 'UTK': {'rank': 194.0, 'name': 'UTRUST'}, 'MYST': {'rank': 433.0, 'name': 'Mysterium'}, 'DASH': {'rank': 12.0, 'name': 'Dash'}, 'INT': {'rank': 279.0, 'name': 'Internet Node Token'}, 'XSH': {'rank': 354.0, 'name': 'SHIELD'}, 'GNT': {'rank': 56.0, 'name': 'Golem'}, 'LBC': {'rank': 162.0, 'name': 'LBRY Credits'}, 'QRL': {'rank': 158.0, 'name': 'Quantum Resistant Ledger'}, 'EVN': {'rank': 184.0, 'name': 'Envion'}, 'SYNX': {'rank': 398.0, 'name': 'Syndicate'}, 'BLUE': {'rank': 463.0, 'name': 'BLUE'}, 'POA': {'rank': 166.0, 'name': 'POA Network'}, 'TNC': {'rank': 221.0, 'name': 'Trinity Network Credit'}, 'DLT': {'rank': 326.0, 'name': 'Agrello'}, 'IXT': {'rank': 411.0, 'name': 'iXledger'}, 'PRL': {'rank': 155.0, 'name': 'Oyster'}, 'SOC': {'rank': 299.0, 'name': 'All Sports'}, 'ADA': {'rank': 6.0, 'name': 'Cardano'}, 'LRC': {'rank': 69.0, 'name': 'Loopring'}, 'FLDC': {'rank': 425.0, 'name': 'FoldingCoin'}, 'SMART': {'rank': 96.0, 'name': 'SmartCash'}, 'IDH': {'rank': 242.0, 'name': 'indaHash'}, 'DCN': {'rank': 86.0, 'name': 'Dentacoin'}, 'XWC': {'rank': 266.0, 'name': 'WhiteCoin'}, 'LET': {'rank': 287.0, 'name': 'LinkEye'}, 'MUE': {'rank': 333.0, 'name': 'MonetaryUnit'}, 'GAS': {'rank': 55.0, 'name': 'Gas'}, 'BOT': {'rank': 372.0, 'name': 'Bodhi'}, 'HPB': {'rank': 139.0, 'name': 'High Performance Blockchain'}, 'IPL': {'rank': 367.0, 'name': 'InsurePal'}, 'PND': {'rank': 460.0, 'name': 'Pandacoin'}, 'TOA': {'rank': 361.0, 'name': 'ToaCoin'}, 'THC': {'rank': 334.0, 'name': 'HempCoin'}, 'BITB': {'rank': 277.0, 'name': 'Bean Cash'}, 'DTB': {'rank': 339.0, 'name': 'Databits'}, 'OAX': {'rank': 345.0, 'name': 'OAX'}, 'B2B': {'rank': 415.0, 'name': 'B2BX'}, 'KNC': {'rank': 72.0, 'name': 'Kyber Network'}, 'EMC2': {'rank': 188.0, 'name': 'Einsteinium'}, 'ZEN': {'rank': 123.0, 'name': 'ZenCash'}, 'AEON': {'rank': 214.0, 'name': 'Aeon'}, 'IOT': {'rank': 11.0, 'name': 'IOTA'}, 'POWR': {'rank': 87.0, 'name': 'Power Ledger'}, 'ION': {'rank': 151.0, 'name': 'ION'}, 'SIB': {'rank': 248.0, 'name': 'SIBCoin'}, 'PLBT': {'rank': 431.0, 'name': 'Polybius'}, 'UNITY': {'rank': 124.0, 'name': 'SuperNET'}, 'ARK': {'rank': 48.0, 'name': 'Ark'}, 'CV': {'rank': 343.0, 'name': 'carVertical'}, 'PPC': {'rank': 174.0, 'name': 'Peercoin'}, 'GNO': {'rank': 100.0, 'name': 'Gnosis'}, 'OMG': {'rank': 22.0, 'name': 'OmiseGO'}, 'MOBI': {'rank': 218.0, 'name': 'Mobius'}, 'UKG': {'rank': 223.0, 'name': 'Unikoin Gold'}, 'POSW': {'rank': 312.0, 'name': 'PoSW Coin'}, 'INCNT': {'rank': 380.0, 'name': 'Incent'}, 'VOX': {'rank': 265.0, 'name': 'Voxels'}, 'EAC': {'rank': 373.0, 'name': 'EarthCoin'}, 'BTC': {'rank': 1.0, 'name': 'Bitcoin'}, 'TRUE': {'rank': 350.0, 'name': 'True Chain'}, 'CMT': {'rank': 193.0, 'name': 'CyberMiles'}, 'SPF': {'rank': 468.0, 'name': 'SportyCo'}, 'VRC': {'rank': 273.0, 'name': 'VeriCoin'}, 'TRAC': {'rank': 213.0, 'name': 'OriginTrail'}, 'CAG': {'rank': 496.0, 'name': 'Change'}, 'MKR': {'rank': 35.0, 'name': 'Maker'}, 'PRE': {'rank': 243.0, 'name': 'Presearch'}, 'ATM': {'rank': 258.0, 'name': 'ATMChain'}, 'CNX': {'rank': 51.0, 'name': 'Cryptonex'}, 'FDX': {'rank': 427.0, 'name': 'FidentiaX'}, 'CS': {'rank': 131.0, 'name': 'Credits'}, 'COSS': {'rank': 271.0, 'name': 'COSS'}, 'NGC': {'rank': 215.0, 'name': 'NAGA'}, 'PURA': {'rank': 128.0, 'name': 'Pura'}, 'CFI': {'rank': 226.0, 'name': 'Cofound.it'}, 'SWT': {'rank': 362.0, 'name': 'Swarm City'}, 'MOT': {'rank': 370.0, 'name': 'Olympus Labs'}, 'MLN': {'rank': 165.0, 'name': 'Melon'}, 'DTR': {'rank': 133.0, 'name': 'Dynamic Trading Rights'}, 'AXP': {'rank': 436.0, 'name': 'aXpire'}, 'KLC': {'rank': 486.0, 'name': 'KiloCoin'}, 'VIA': {'rank': 182.0, 'name': 'Viacoin'}, 'AID': {'rank': 494.0, 'name': 'AidCoin'}, 'MEE': {'rank': 473.0, 'name': 'CoinMeet'}, 'NEBL': {'rank': 84.0, 'name': 'Neblio'}, 'HOT': {'rank': 432.0, 'name': 'Hydro Protocol'}, 'GXS': {'rank': 78.0, 'name': 'GXShares'}, 'CVCOIN': {'rank': 495.0, 'name': 'CVCoin'}, 'UBQ': {'rank': 117.0, 'name': 'Ubiq'}, 'DIME': {'rank': 289.0, 'name': 'Dimecoin'}, 'DYN': {'rank': 412.0, 'name': 'Dynamic'}, 'NAS': {'rank': 71.0, 'name': 'Nebulas'}, 'RNT': {'rank': 418.0, 'name': 'OneRoot Network'}, 'REBL': {'rank': 451.0, 'name': 'Rebellious'}, 'WABI': {'rank': 199.0, 'name': 'WaBi'}, 'ITC': {'rank': 169.0, 'name': 'IoT Chain'}, 'AST': {'rank': 203.0, 'name': 'AirSwap'}, 'TIPS': {'rank': 484.0, 'name': 'FedoraCoin'}, 'JNT': {'rank': 189.0, 'name': 'Jibrel Network'}, 'BTO': {'rank': 228.0, 'name': 'Bottos'}, 'STX': {'rank': 390.0, 'name': 'Stox'}, 'BCO': {'rank': 152.0, 'name': 'BridgeCoin'}, 'DGD': {'rank': 25.0, 'name': 'DigixDAO'}, 'BIX': {'rank': 176.0, 'name': 'Bibox Token'}, 'XLM': {'rank': 8.0, 'name': 'Stellar'}, 'FTC': {'rank': 211.0, 'name': 'Feathercoin'}, 'BITUSD': {'rank': 395.0, 'name': 'bitUSD'}, 'DOGE': {'rank': 38.0, 'name': 'Dogecoin'}, 'KRM': {'rank': 477.0, 'name': 'Karma'}, 'ZPT': {'rank': 314.0, 'name': 'Zeepin'}, 'QBT': {'rank': 285.0, 'name': 'Qbao'}, 'POT': {'rank': 257.0, 'name': 'PotCoin'}, 'CVC': {'rank': 122.0, 'name': 'Civic'}, 'WAX': {'rank': 109.0, 'name': 'WAX'}, 'CAT': {'rank': 437.0, 'name': 'BlockCAT'}, 'WPR': {'rank': 198.0, 'name': 'WePower'}, 'DAI': {'rank': 337.0, 'name': 'Dai'}, 'ALIS': {'rank': 392.0, 'name': 'ALIS'}, 'LSK': {'rank': 21.0, 'name': 'Lisk'}, 'AURA': {'rank': 319.0, 'name': 'Aurora DAO'}, 'NET': {'rank': 267.0, 'name': 'Nimiq'}, 'SWFTC': {'rank': 315.0, 'name': 'SwftCoin'}, 'ZOI': {'rank': 306.0, 'name': 'Zoin'}, 'MCO': {'rank': 116.0, 'name': 'Monaco'}, 'XTO': {'rank': 303.0, 'name': 'Tao'}, 'STORJ': {'rank': 102.0, 'name': 'Storj'}, 'COVAL': {'rank': 445.0, 'name': 'Circuits of Value'}, 'AMB': {'rank': 173.0, 'name': 'Ambrosus'}, 'HST': {'rank': 205.0, 'name': 'Decision Token'}, 'DMD': {'rank': 282.0, 'name': 'Diamond'}, 'SXDT': {'rank': 262.0, 'name': 'Spectre.ai Dividend Token'}, 'OTN': {'rank': 389.0, 'name': 'Open Trading Network'}, 'BTG': {'rank': 20.0, 'name': 'Bitcoin Gold'}, 'NTRN': {'rank': 408.0, 'name': 'Neutron'}, 'ONION': {'rank': 259.0, 'name': 'DeepOnion'}, 'BCC': {'rank': 347.0, 'name': 'BitConnect'}, 'OCN': {'rank': 264.0, 'name': 'Odyssey'}, 'CAN': {'rank': 353.0, 'name': 'CanYaCoin'}, 'FCT': {'rank': 64.0, 'name': 'Factom'}, 'USNBT': {'rank': 456.0, 'name': 'NuBits'}, 'GRS': {'rank': 224.0, 'name': 'Groestlcoin'}, 'COB': {'rank': 196.0, 'name': 'Cobinhood'}, 'OMNI': {'rank': 335.0, 'name': 'Omni'}, 'ICN': {'rank': 75.0, 'name': 'Iconomi'}, 'VEN': {'rank': 17.0, 'name': 'VeChain'}, 'SALT': {'rank': 77.0, 'name': 'SALT'}, 'NXC': {'rank': 400.0, 'name': 'Nexium'}, 'MDS': {'rank': 137.0, 'name': 'MediShares'}, 'ECN': {'rank': 446.0, 'name': 'E-coin'}, 'NVC': {'rank': 469.0, 'name': 'Novacoin'}, 'RVT': {'rank': 376.0, 'name': 'Rivetz'}, 'SHIFT': {'rank': 230.0, 'name': 'Shift'}, 'TIME': {'rank': 308.0, 'name': 'Chronobank'}, 'FSN': {'rank': 146.0, 'name': 'Fusion'}, 'BLZ': {'rank': 160.0, 'name': 'Bluzelle'}, 'TX': {'rank': 430.0, 'name': 'TransferCoin'}, 'PAY': {'rank': 91.0, 'name': 'TenX'}, 'DBC': {'rank': 179.0, 'name': 'DeepBrain Chain'}, 'CPC': {'rank': 220.0, 'name': 'CPChain'}, 'MINT': {'rank': 296.0, 'name': 'Mintcoin'}, 'ETH': {'rank': 2.0, 'name': 'Ethereum'}, 'PZM': {'rank': 414.0, 'name': 'PRIZM'}, 'MUSIC': {'rank': 391.0, 'name': 'Musicoin'}, 'XDN': {'rank': 126.0, 'name': 'DigitalNote'}, 'NXT': {'rank': 90.0, 'name': 'Nxt'}, 'EDR': {'rank': 349.0, 'name': 'E-Dinar Coin'}, 'BTCZ': {'rank': 500.0, 'name': 'BitcoinZ'}, 'BTCD': {'rank': 107.0, 'name': 'BitcoinDark'}, 'BCPT': {'rank': 231.0, 'name': 'BlockMason Credit Protocol'}, 'NULS': {'rank': 135.0, 'name': 'Nuls'}, 'ADX': {'rank': 147.0, 'name': 'AdEx'}, 'RADS': {'rank': 328.0, 'name': 'Radium'}, 'MANA': {'rank': 118.0, 'name': 'Decentraland'}, 'ARDR': {'rank': 49.0, 'name': 'Ardor'}, 'XCP': {'rank': 206.0, 'name': 'Counterparty'}, 'RDD': {'rank': 74.0, 'name': 'ReddCoin'}, 'AUR': {'rank': 364.0, 'name': 'Auroracoin'}, 'LEO': {'rank': 297.0, 'name': 'LEOcoin'}, 'SNOV': {'rank': 405.0, 'name': 'Snovio'}, 'GUP': {'rank': 292.0, 'name': 'Matchpool'}, 'SPC': {'rank': 177.0, 'name': 'SpaceChain'}, 'HMC': {'rank': 309.0, 'name': 'Hi Mutual Society'}, 'TRST': {'rank': 284.0, 'name': 'WeTrust'}, 'TAAS': {'rank': 208.0, 'name': 'TaaS'}, 'XZC': {'rank': 80.0, 'name': 'ZCoin'}, 'DIVX': {'rank': 383.0, 'name': 'Divi'}, 'PIVX': {'rank': 59.0, 'name': 'PIVX'}, 'SLS': {'rank': 121.0, 'name': 'SaluS'}, 'UQC': {'rank': 311.0, 'name': 'Uquid Coin'}, 'RMC': {'rank': 388.0, 'name': 'Russian Miner Coin'}, 'PLU': {'rank': 475.0, 'name': 'Pluton'}, 'XVC': {'rank': 481.0, 'name': 'Vcash'}, 'FLIXX': {'rank': 478.0, 'name': 'Flixxo'}, 'ACT': {'rank': 140.0, 'name': 'Achain'}, 'ORME': {'rank': 261.0, 'name': 'Ormeus Coin'}, 'TNT': {'rank': 229.0, 'name': 'Tierion'}, 'IOP': {'rank': 441.0, 'name': 'Internet of People'}, 'LOC': {'rank': 443.0, 'name': 'LockChain'}, 'BCY': {'rank': 455.0, 'name': 'Bitcrystals'}, 'POLY': {'rank': 88.0, 'name': 'Polymath'}, 'EKO': {'rank': 440.0, 'name': 'EchoLink'}, 'GBYTE': {'rank': 67.0, 'name': 'Byteball Bytes'}, 'WGR': {'rank': 178.0, 'name': 'Wagerr'}, 'VIBE': {'rank': 170.0, 'name': 'VIBE'}, 'FUEL': {'rank': 209.0, 'name': 'Etherparty'}, 'EVR': {'rank': 322.0, 'name': 'Everus'}, 'BBR': {'rank': 422.0, 'name': 'Boolberry'}, 'BTS': {'rank': 40.0, 'name': 'BitShares'}, 'ZRX': {'rank': 44.0, 'name': '0x'}, 'SNM': {'rank': 180.0, 'name': 'SONM'}, 'XMR': {'rank': 9.0, 'name': 'Monero'}, 'HKN': {'rank': 381.0, 'name': 'Hacken'}, 'DNA': {'rank': 377.0, 'name': 'EncrypGen'}, 'MDT': {'rank': 421.0, 'name': 'Measurable Data Token'}, 'PART': {'rank': 66.0, 'name': 'Particl'}, 'BNTY': {'rank': 459.0, 'name': 'Bounty0x'}, 'LEV': {'rank': 447.0, 'name': 'Leverj'}, 'CDT': {'rank': 240.0, 'name': 'CoinDash'}, 'PRA': {'rank': 434.0, 'name': 'ProChain'}, 'LUX': {'rank': 428.0, 'name': 'LUXCoin'}, 'HEAT': {'rank': 479.0, 'name': 'HEAT'}, 'SBD': {'rank': 254.0, 'name': 'Steem Dollars'}, 'NVST': {'rank': 438.0, 'name': 'NVO'}, 'MGO': {'rank': 181.0, 'name': 'MobileGo'}, 'WINGS': {'rank': 171.0, 'name': 'Wings'}, 'TRX': {'rank': 14.0, 'name': 'TRON'}, 'NIO': {'rank': 492.0, 'name': 'Autonio'}, 'SXUT': {'rank': 471.0, 'name': 'Spectre.ai Utility Token'}, 'DPY': {'rank': 207.0, 'name': 'Delphy'}, 'HBT': {'rank': 416.0, 'name': 'Hubii Network'}, 'DGB': {'rank': 58.0, 'name': 'DigiByte'}, 'KEY': {'rank': 316.0, 'name': 'Selfkey'}, 'BAT': {'rank': 53.0, 'name': 'Basic Attention Token'}, 'SAN': {'rank': 113.0, 'name': 'Santiment Network Token'}, 'CRPT': {'rank': 252.0, 'name': 'Crypterium'}, 'ZCL': {'rank': 219.0, 'name': 'ZClassic'}, 'LUN': {'rank': 225.0, 'name': 'Lunyr'}, 'CTR': {'rank': 236.0, 'name': 'Centra'}, 'BSD': {'rank': 360.0, 'name': 'BitSend'}, 'BLT': {'rank': 276.0, 'name': 'Bloom'}, 'SAFEX': {'rank': 244.0, 'name': 'Safe Exchange Coin'}, 'QLC': {'rank': 256.0, 'name': 'QLINK'}, 'GTO': {'rank': 210.0, 'name': 'Gifto'}, 'ECA': {'rank': 342.0, 'name': 'Electra'}, 'ZIL': {'rank': 61.0, 'name': 'Zilliqa'}, 'KIN': {'rank': 76.0, 'name': 'Kin'}, 'PTOY': {'rank': 410.0, 'name': 'Patientory'}, 'XMY': {'rank': 382.0, 'name': 'Myriad'}, 'AVT': {'rank': 480.0, 'name': 'Aventus'}, 'EXP': {'rank': 305.0, 'name': 'Expanse'}, 'GVT': {'rank': 105.0, 'name': 'Genesis Vision'}, 'IFT': {'rank': 338.0, 'name': 'InvestFeed'}, 'GBX': {'rank': 483.0, 'name': 'GoByte'}, 'XPM': {'rank': 355.0, 'name': 'Primecoin'}, 'LINDA': {'rank': 489.0, 'name': 'Linda'}, 'RLC': {'rank': 134.0, 'name': 'iExec RLC'}, 'MSP': {'rank': 307.0, 'name': 'Mothership'}, 'HTML': {'rank': 197.0, 'name': 'HTMLCOIN'}, 'HSR': {'rank': 54.0, 'name': 'Hshare'}, 'ABY': {'rank': 498.0, 'name': 'ArtByte'}, 'EMC': {'rank': 97.0, 'name': 'Emercoin'}, 'VOISE': {'rank': 465.0, 'name': 'Voise'}, 'KORE': {'rank': 457.0, 'name': 'Kore'}, 'UCASH': {'rank': 237.0, 'name': 'U.CASH'}, 'MTN': {'rank': 239.0, 'name': 'Medicalchain'}, 'PFR': {'rank': 464.0, 'name': 'Payfair'}, 'PARETO': {'rank': 344.0, 'name': 'Pareto Network'}, 'SNT': {'rank': 34.0, 'name': 'Status'}, 'DEW': {'rank': 164.0, 'name': 'DEW'}, 'TSL': {'rank': 321.0, 'name': 'Energo'}, 'ETHOS': {'rank': 57.0, 'name': 'Ethos'}, 'BDG': {'rank': 374.0, 'name': 'BitDegree'}, 'AGRS': {'rank': 159.0, 'name': 'Agoras Tokens'}, 'NXS': {'rank': 79.0, 'name': 'Nexus'}, 'CLAM': {'rank': 397.0, 'name': 'Clams'}, 'ICX': {'rank': 24.0, 'name': 'ICON'}, 'HMQ': {'rank': 235.0, 'name': 'Humaniq'}, 'XRL': {'rank': 387.0, 'name': 'Rialto'}, 'SUB': {'rank': 132.0, 'name': 'Substratum'}, 'USDT': {'rank': 16.0, 'name': 'Tether'}, 'COLX': {'rank': 278.0, 'name': 'ColossusCoinXT'}, 'PRO': {'rank': 356.0, 'name': 'Propy'}, 'RDN': {'rank': 112.0, 'name': 'Raiden Network Token'}, 'FLASH': {'rank': 247.0, 'name': 'Flash'}, 'ELIX': {'rank': 499.0, 'name': 'Elixir'}, 'QTUM': {'rank': 18.0, 'name': 'Qtum'}, 'PEPECASH': {'rank': 260.0, 'name': 'Pepe Cash'}, 'INK': {'rank': 187.0, 'name': 'Ink'}, 'TEL': {'rank': 150.0, 'name': 'Telcoin'}, 'CREDO': {'rank': 424.0, 'name': 'Credo'}, 'XUC': {'rank': 407.0, 'name': 'Exchange Union'}, 'KCS': {'rank': 60.0, 'name': 'KuCoin Shares'}, 'SPANK': {'rank': 175.0, 'name': 'SpankChain'}, 'R': {'rank': 73.0, 'name': 'Revain'}, 'ARN': {'rank': 300.0, 'name': 'Aeron'}, 'BIO': {'rank': 474.0, 'name': 'BioCoin'}, 'BTM': {'rank': 46.0, 'name': 'Bytom'}, 'QAU': {'rank': 403.0, 'name': 'Quantum'}, 'NYC': {'rank': 346.0, 'name': 'NewYorkCoin'}, 'GOLOS': {'rank': 385.0, 'name': 'Golos'}, 'WAVES': {'rank': 32.0, 'name': 'Waves'}, 'SPHTX': {'rank': 142.0, 'name': 'SophiaTX'}, 'SNC': {'rank': 288.0, 'name': 'SunContract'}, 'OST': {'rank': 153.0, 'name': 'Simple Token'}, 'EDG': {'rank': 157.0, 'name': 'Edgeless'}, 'WCT': {'rank': 351.0, 'name': 'Waves Community Token'}, 'POE': {'rank': 130.0, 'name': 'Po.et'}, 'TIX': {'rank': 318.0, 'name': 'Blocktix'}, 'EOS': {'rank': 10.0, 'name': 'EOS'}, 'SPHR': {'rank': 442.0, 'name': 'Sphere'}, 'LKK': {'rank': 280.0, 'name': 'Lykke'}, 'AGI': {'rank': 98.0, 'name': 'SingularityNET'}, 'AMP': {'rank': 212.0, 'name': 'Synereo'}, 'ADT': {'rank': 216.0, 'name': 'adToken'}, 'MDA': {'rank': 323.0, 'name': 'Moeda Loyalty Points'}, 'ZEC': {'rank': 23.0, 'name': 'Zcash'}, 'XLR': {'rank': 435.0, 'name': 'Solaris'}, 'BCN': {'rank': 28.0, 'name': 'Bytecoin'}, 'LEND': {'rank': 148.0, 'name': 'ETHLend'}, 'FAIR': {'rank': 313.0, 'name': 'FairCoin'}, 'TIO': {'rank': 324.0, 'name': 'Trade Token'}, 'DATA': {'rank': 191.0, 'name': 'Streamr DATAcoin'}, 'BIS': {'rank': 406.0, 'name': 'Bismuth'}, 'HAC': {'rank': 420.0, 'name': 'Hackspace Capital'}, 'RPX': {'rank': 154.0, 'name': 'Red Pulse'}, 'VTC': {'rank': 103.0, 'name': 'Vertcoin'}, '1ST': {'rank': 293.0, 'name': 'FirstBlood'}, 'MOON': {'rank': 270.0, 'name': 'Mooncoin'}, 'CHIPS': {'rank': 470.0, 'name': 'CHIPS'}, 'DADI': {'rank': 298.0, 'name': 'DADI'}, 'XRB': {'rank': 19.0, 'name': 'Nano'}, 'CLOAK': {'rank': 168.0, 'name': 'CloakCoin'}, 'RBY': {'rank': 371.0, 'name': 'Rubycoin'}, 'HORSE': {'rank': 458.0, 'name': 'Ethorse'}, 'SRN': {'rank': 101.0, 'name': 'SIRIN LABS Token'}, 'VIB': {'rank': 234.0, 'name': 'Viberate'}, 'CND': {'rank': 94.0, 'name': 'Cindicator'}, 'ZSC': {'rank': 295.0, 'name': 'Zeusshield'}, 'XEL': {'rank': 291.0, 'name': 'Elastic'}, 'POLIS': {'rank': 450.0, 'name': 'Polis'}, 'STEEM': {'rank': 27.0, 'name': 'Steem'}, 'PPT': {'rank': 29.0, 'name': 'Populous'}, 'MAID': {'rank': 92.0, 'name': 'MaidSafeCoin'}, 'ETP': {'rank': 202.0, 'name': 'Metaverse ETP'}, 'PST': {'rank': 386.0, 'name': 'Primas'}, 'SLR': {'rank': 340.0, 'name': 'SolarCoin'}, 'IOC': {'rank': 249.0, 'name': 'I/O Coin'}, 'QUN': {'rank': 327.0, 'name': 'QunQun'}, 'AIR': {'rank': 379.0, 'name': 'AirToken'}, 'XBY': {'rank': 201.0, 'name': 'XTRABYTES'}, 'BURST': {'rank': 183.0, 'name': 'Burst'}, 'FUN': {'rank': 70.0, 'name': 'FunFair'}, 'WTC': {'rank': 37.0, 'name': 'Waltonchain'}, 'CHSB': {'rank': 331.0, 'name': 'SwissBorg'}, 'KMD': {'rank': 47.0, 'name': 'Komodo'}, 'TCC': {'rank': 444.0, 'name': 'The ChampCoin'}, 'NEU': {'rank': 375.0, 'name': 'Neumark'}, 'XAS': {'rank': 144.0, 'name': 'Asch'}, 'ESP': {'rank': 426.0, 'name': 'Espers'}, 'ALQO': {'rank': 330.0, 'name': 'ALQO'}, 'REM': {'rank': 363.0, 'name': 'Remme'}, 'CXO': {'rank': 454.0, 'name': 'CargoX'}, 'EBTC': {'rank': 476.0, 'name': 'eBitcoin'}, 'VEE': {'rank': 145.0, 'name': 'BLOCKv'}, 'IGNIS': {'rank': 115.0, 'name': 'Ignis'}, 'PUT': {'rank': 429.0, 'name': 'Profile Utility Token'}, 'HGT': {'rank': 485.0, 'name': 'HelloGold'}, 'MOD': {'rank': 222.0, 'name': 'Modum'}, 'UTNP': {'rank': 190.0, 'name': 'Universa'}, 'QASH': {'rank': 68.0, 'name': 'QASH'}, 'PIRL': {'rank': 487.0, 'name': 'Pirl'}, 'ANT': {'rank': 111.0, 'name': 'Aragon'}, 'DTA': {'rank': 185.0, 'name': 'DATA'}, 'KICK': {'rank': 246.0, 'name': 'KickCoin'}, 'MTH': {'rank': 290.0, 'name': 'Monetha'}, 'XEM': {'rank': 13.0, 'name': 'NEM'}, 'APPC': {'rank': 192.0, 'name': 'AppCoins'}, 'FLO': {'rank': 369.0, 'name': 'FlorinCoin'}, 'STRAT': {'rank': 30.0, 'name': 'Stratis'}, 'SC': {'rank': 36.0, 'name': 'Siacoin'}, 'PHR': {'rank': 366.0, 'name': 'Phore'}, 'DRGN': {'rank': 50.0, 'name': 'Dragonchain'}, 'YOYOW': {'rank': 304.0, 'name': 'YOYOW'}, 'MED': {'rank': 149.0, 'name': 'MediBloc'}, 'STORM': {'rank': 127.0, 'name': 'Storm'}, 'OXY': {'rank': 490.0, 'name': 'Oxycoin'}, 'WRC': {'rank': 452.0, 'name': 'Worldcore'}, 'BCH': {'rank': 4.0, 'name': 'Bitcoin Cash'}, 'ABT': {'rank': 138.0, 'name': 'Arcblock'}, 'XPA': {'rank': 129.0, 'name': 'XPA'}, 'LINK': {'rank': 83.0, 'name': 'ChainLink'}, 'CURE': {'rank': 449.0, 'name': 'Curecoin'}, 'OBITS': {'rank': 482.0, 'name': 'OBITS'}, 'COV': {'rank': 348.0, 'name': 'Covesting'}, 'ICOS': {'rank': 352.0, 'name': 'ICOS'}, 'SOAR': {'rank': 283.0, 'name': 'Soarcoin'}, 'MNX': {'rank': 136.0, 'name': 'MinexCoin'}, 'EVX': {'rank': 268.0, 'name': 'Everex'}, 'SKY': {'rank': 120.0, 'name': 'Skycoin'}, 'TAU': {'rank': 294.0, 'name': 'Lamden'}, 'GTC': {'rank': 325.0, 'name': 'Game.com'}, 'LTC': {'rank': 5.0, 'name': 'Litecoin'}, 'OK': {'rank': 359.0, 'name': 'OKCash'}, 'NEOS': {'rank': 402.0, 'name': 'NeosCoin'}, 'ATMS': {'rank': 467.0, 'name': 'Atmos'}, 'ELF': {'rank': 65.0, 'name': 'aelf'}, 'BLK': {'rank': 275.0, 'name': 'BlackCoin'}, 'ENG': {'rank': 95.0, 'name': 'Enigma'}, 'DICE': {'rank': 409.0, 'name': 'Etheroll'}, 'SYS': {'rank': 52.0, 'name': 'Syscoin'}, 'GAME': {'rank': 104.0, 'name': 'GameCredits'}, 'BLOCK': {'rank': 85.0, 'name': 'Blocknet'}, 'QSP': {'rank': 110.0, 'name': 'Quantstamp'}, 'LMC': {'rank': 358.0, 'name': 'LoMoCoin'}, 'TKN': {'rank': 241.0, 'name': 'TokenCard'}, 'OCT': {'rank': 404.0, 'name': 'OracleChain'}, 'PLR': {'rank': 99.0, 'name': 'Pillar'}, 'ENRG': {'rank': 368.0, 'name': 'Energycoin'}, 'BAY': {'rank': 163.0, 'name': 'BitBay'}, 'COFI': {'rank': 439.0, 'name': 'CoinFi'}, 'PASC': {'rank': 332.0, 'name': 'Pascal Coin'}, 'CSNO': {'rank': 401.0, 'name': 'BitDice'}, 'VERI': {'rank': 43.0, 'name': 'Veritaseum'}, 'XP': {'rank': 156.0, 'name': 'Experience Points'}, 'DBET': {'rank': 394.0, 'name': 'DecentBet'}, 'XAUR': {'rank': 413.0, 'name': 'Xaurum'}, 'RHOC': {'rank': 33.0, 'name': 'RChain'}, 'HVN': {'rank': 245.0, 'name': 'Hive Project'}, 'DENT': {'rank': 81.0, 'name': 'Dent'}, 'PKT': {'rank': 493.0, 'name': 'Playkey'}, 'NLG': {'rank': 200.0, 'name': 'Gulden'}, 'SNGLS': {'rank': 186.0, 'name': 'SingularDTV'}, 'UNIT': {'rank': 378.0, 'name': 'Universal Currency'}, 'BITCNY': {'rank': 250.0, 'name': 'bitCNY'}, 'DAT': {'rank': 251.0, 'name': 'Datum'}, 'ART': {'rank': 329.0, 'name': 'Maecenas'}, 'DRT': {'rank': 357.0, 'name': 'DomRaider'}, 'DCR': {'rank': 39.0, 'name': 'Decred'}, 'SWM': {'rank': 274.0, 'name': 'Swarm'}, 'XSPEC': {'rank': 393.0, 'name': 'Spectrecoin'}, 'BRD': {'rank': 195.0, 'name': 'Bread'}, 'ZAP': {'rank': 286.0, 'name': 'Zap'}, 'LA': {'rank': 336.0, 'name': 'LATOKEN'}, 'BTX': {'rank': 106.0, 'name': 'Bitcore'}, 'EDO': {'rank': 172.0, 'name': 'Eidoo'}, 'LOCI': {'rank': 491.0, 'name': 'LOCIcoin'}, 'PRG': {'rank': 399.0, 'name': 'Paragon'}, 'INS': {'rank': 204.0, 'name': 'INS Ecosystem'}, 'CAPP': {'rank': 281.0, 'name': 'Cappasity'}, 'BMC': {'rank': 320.0, 'name': 'Blackmoon'}, 'BPT': {'rank': 269.0, 'name': 'Blockport'}, 'RCN': {'rank': 167.0, 'name': 'Ripio Credit Network'}, 'DNT': {'rank': 217.0, 'name': 'district0x'}, 'SEQ': {'rank': 488.0, 'name': 'Sequence'}, 'ECC': {'rank': 232.0, 'name': 'ECC'}, 'NEO': {'rank': 7.0, 'name': 'NEO'}, 'CRW': {'rank': 227.0, 'name': 'Crown'}, 'AE': {'rank': 41.0, 'name': 'Aeternity'}, 'XVG': {'rank': 31.0, 'name': 'Verge'}, 'ETC': {'rank': 15.0, 'name': 'Ethereum Classic'}, 'THETA': {'rank': 119.0, 'name': 'Theta Token'}, 'ATB': {'rank': 417.0, 'name': 'ATBCoin'}, 'ASTRO': {'rank': 497.0, 'name': 'Astro'}, 'REP': {'rank': 42.0, 'name': 'Augur'}, 'MONA': {'rank': 63.0, 'name': 'MonaCoin'}, 'DRP': {'rank': 466.0, 'name': 'DCORP'}, 'NAV': {'rank': 125.0, 'name': 'NavCoin'}, 'DCT': {'rank': 233.0, 'name': 'DECENT'}, 'PPY': {'rank': 341.0, 'name': 'Peerplays'}, 'GRC': {'rank': 310.0, 'name': 'GridCoin'}, 'REQ': {'rank': 93.0, 'name': 'Request Network'}, 'TGT': {'rank': 384.0, 'name': 'Target Coin'}, 'GAM': {'rank': 396.0, 'name': 'Gambit'}, 'TNB': {'rank': 141.0, 'name': 'Time New Bank'}, 'TIE': {'rank': 419.0, 'name': 'Ties.DB'}, 'PPP': {'rank': 143.0, 'name': 'PayPie'}, 'DBIX': {'rank': 448.0, 'name': 'DubaiCoin'}, 'STK': {'rank': 302.0, 'name': 'STK'}, 'MER': {'rank': 272.0, 'name': 'Mercury'}, 'XRP': {'rank': 3.0, 'name': 'Ripple'}, 'IOST': {'rank': 82.0, 'name': 'IOStoken'}, 'UNO': {'rank': 253.0, 'name': 'Unobtanium'}, 'XST': {'rank': 472.0, 'name': 'Stealthcoin'}, 'MTL': {'rank': 114.0, 'name': 'Metal'}, 'BQ': {'rank': 462.0, 'name': 'bitqy'}, 'ENJ': {'rank': 108.0, 'name': 'Enjin Coin'}, 'PINK': {'rank': 461.0, 'name': 'PinkCoin'}, 'GCR': {'rank': 423.0, 'name': 'Global Currency Reserve'}, 'NMC': {'rank': 263.0, 'name': 'Namecoin'}, 'BNT': {'rank': 89.0, 'name': 'Bancor'}, 'ETN': {'rank': 45.0, 'name': 'Electroneum'}, 'NMR': {'rank': 255.0, 'name': 'Numeraire'}, 'MYB': {'rank': 453.0, 'name': 'MyBit Token'}, 'GRID': {'rank': 301.0, 'name': 'Grid+'}, 'BNB': {'rank': 26.0, 'name': 'Binance Coin'}, 'NLC2': {'rank': 317.0, 'name': 'NoLimitCoin'}}
currencies = ["INR", "USD", "GBP", "EUR", "JPY", "CNY", "SGD", "ZAR", "BTC", "ETH", "CAD", "AUD", "TRY", "AED"]
btc_markets = {"INR": {
                    "Zebpay": "zebpay_new/BTC",
                    "LocalBitcoins": "localbitcoins_BTC_INR",
                    "Coinsecure": "coinsecure",
                    "PocketBits": "pocketbits",
                    "Koinex": "koinex_BTC_INR",
                    "Throughbit": "throughbit_BTC_INR",
                    "Bitbns": "bitbns_BTC_INR",
                    "Coinome": "coinome_BTC_INR",
                    "Coindelta": "coindelta/BTC/INR"
                }, "USD": {
                    "Coinbase": "coinbase_BTC_USD",
                    "Kraken": "kraken_BTC_USD",
                    "Gemini": "gemini_BTC_USD",
                    "LocalBitcoins": "localbitcoins_BTC_USD",
                    "Bitfinex": "bitfinex_BTC_USD",
                    "Bitstamp": "bitstamp_BTC_USD",
                    "Kucoin": "kucoin/BTC/USDT"
                }, "GBP": {
                    "Coinbase": "coinbase_BTC_GBP",
                    "Kraken": "kraken_BTC_GBP",
                    "LocalBitcoins": "localbitcoins_BTC_GBP"
                }, "EUR": {
                   "Coinbase": "coinbase_BTC_EUR",
                   "LocalBitcoins": "localbitcoins_BTC_EUR",
                   "Kraken": "kraken_BTC_EUR"
                }, "JPY": {
                    "Kraken": "kraken_BTC_JPY"
                }, "CNY": {
                    "LocalBitcoins": "localbitcoins_BTC_CNY"
                }, "SGD": {
                    "LocalBitcoins": "localbitcoins_BTC_SGD"
                }, "ZAR": {
                    "LocalBitcoins": "localbitcoins_BTC_ZAR"
                }, "BTC": {}, "ETH": {}, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}}

eth_markets = {"INR": {
                    "Koinex": "koinex_ETH_INR",
                    "Throughbit": "throughbit_ETH_INR",
                    "Bitbns": "bitbns_ETH_INR",
                    "Coindelta": "coindelta/ETH/INR",
                    "Zebpay": "zebpay_new/ETH"
                }, "USD": {
                    "Coinbase": "coinbase_ETH_USD",
                    "Kraken": "kraken_ETH_USD",
                    "Gemini": "gemini_ETH_USD",
                    "Bitfinex": "bitfinex_ETH_USD",
                    "Bitstamp": "bitstamp_ETH_USD",
                    "Kucoin": "kucoin/ETH/USDT"
                },  "GBP": {
                    "Kraken": "kraken_ETH_GBP"
                }, "EUR": {
                    "Coinbase": "coinbase_ETH_EUR",
                    "Bitstamp": "bitstamp_ETH_EUR",
                    "Kraken": "kraken_ETH_EUR"
                },  "JPY": {
                    "Kraken": "kraken_ETH_JPY"
                }, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/ETH/BTC",
                    "Coindelta": "coindelta/ETH/BTC"
                },
                "ETH": {}, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
                }

ltc_markets = {"INR": {
                    "Zebpay": "zebpay_new/LTC",
                    "Koinex": "koinex_LTC_INR",
                    "Coinome": "coinome_LTC_INR",
                    "Coindelta": "coindelta/LTC/INR",
                    "Bitbns": "bitbns_LTC_INR"
                }, "USD": {
                    "Coinbase": "coinbase_LTC_USD",
                    "Kraken": "kraken_LTC_USD",
                    "Bitfinex": "bitfinex_LTC_USD",
                    "Bitstamp": "bitstamp_LTC_USD",
                    "Kucoin": "kucoin/LTC/USDT"
                }, "GBP": {},
                "EUR": {
                    "Coinbase": "coinbase_LTC_EUR",
                    "Bitstamp": "bitstamp_LTC_EUR",
                    "Kraken": "kraken_LTC_EUR"
                },
                "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/LTC/BTC",
                    "Coindelta": "coindelta/LTC/BTC"
                },
                "ETH": {
                    "Kucoin": "kucoin/LTC/ETH"
                }, "CAD": {}, "TRY": {}, "AUD": {}, "AED": {}}

xrp_markets = {"INR": {
                    "Zebpay": "zebpay_new/XRP",
                    "Koinex": "koinex_XRP_INR",
                    "Bitbns": "bitbns_XRP_INR",
                    "Coindelta": "coindelta/XRP/INR"
                },  "USD": {
                    "Bitfinex": "bitfinex_XRP_USD",
                    "Bitstamp": "bitstamp_XRP_USD"
                }, "GBP": {

                }, "EUR": {
                    "Bitstamp": "bitstamp_XRP_EUR",
                },  "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Coindelta": "coindelta/XRP/BTC"
                },
                "ETH": {}, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}}

bch_markets = {"INR": {
                    "Zebpay": "zebpay_new/BCH",
                    "Koinex": "koinex_BCH_INR",
                    "Coinome": "coinome_BCH_INR",
                    "Coindelta": "coindelta/BCH/INR",
                    "Bitbns": "bitbns_BCH_INR",
                }, "USD": {
                    "Bitfinex": "bitfinex_BCH_USD",
                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/BCH/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/BCH/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}}

omg_markets = { "INR": {
                    "Koinex": "koinex_OMG_INR",
                    "Coindelta": "coindelta/OMG/INR"
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/OMG/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/OMG/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

req_markets = { "INR": {
                    "Koinex": "koinex_REQ_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/REQ/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/REQ/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

zrx_markets = { "INR": {
                    "Koinex": "koinex_ZRX_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

gnt_markets = { "INR": {
                    "Koinex": "koinex_GNT_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

bat_markets = { "INR": {
                    "Koinex": "koinex_BAT_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                }, "ETH": {
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

ae_markets = { "INR": {
                    "Koinex": "koinex_AE_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

rpx_markets = { "INR": {
                    "Bitbns": "bitbns_RPX_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/RPX/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/RPX/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
dbc_markets = { "INR": {
                    "Bitbns": "bitbns_DBC_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/DBC/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/DBC/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
xmr_markets = { "INR": {
                    "Bitbns": "bitbns_XMR_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
doge_markets = { "INR": {
                    "Bitbns": "bitbns_DOGE_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }
sia_markets = { "INR": {
                    "Bitbns": "bitbns_SIA_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

xlm_markets = { "INR": {
                    "Bitbns": "bitbns_XLM_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {

                }, "ETH": {

                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

neo_markets = { "INR": {
                    "Bitbns": "bitbns_NEO_INR",
                }, "USD": {

                }, "GBP": {}, "EUR": {}, "JPY": {}, "CNY": {}, "SGD": {}, "ZAR": {},
                "BTC": {
                    "Kucoin": "kucoin/NEO/BTC"
                }, "ETH": {
                    "Kucoin": "kucoin/NEO/ETH"
                }, "CAD": {}, "AUD": {}, "TRY": {}, "AED": {}
            }

indian_crypto_list = ["BTC", "BCH", "ETH", "XRP", "LTC", "OMG", "REQ", "ZRX", "GNT", "BAT", "AE", "RPX", "DBC", "XMR",
                      "DOGE", "SIA", "XLM", "NEO"]

def get_current_crypto_price():
    dict = get_list_of_coins_with_rank()
    if dict is not None:
        crypto_list = list()
        for i in dict.keys():
             crypto_list.append(i)

        crypto_list_string = list()

        if len(crypto_list) > 60:
            crypto_list_chunks = list(chunks(crypto_list, 50))
            for index, value in enumerate(crypto_list_chunks):
                crypto_list_string.append(",".join(value))
        else:
            crypto_list_string.append(",".join(crypto_list))

        currency_list_string = ",".join(currencies)

        exchange_rate_url = "https://api.fixer.io/latest?symbols=INR&base=USD"
        r = requests.get(exchange_rate_url)
        if r.status_code == 200:
            exchange_json = r.json()
            rate = exchange_json["rates"]["INR"]

        for index, value in enumerate(crypto_list_string):
            url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(crypto_list_string[index], currency_list_string)
            print(url)
            r = requests.get(url)
            if r.status_code == 200:
                json = r.json()
                data = json["RAW"]
                for crypto in crypto_list:
                    for currency in currencies:
                        dict[crypto][currency] = {}
                        if crypto in data and currency in data[crypto]:
                            if currency == "INR" and crypto in indian_crypto_list:
                                old_price = db.child(crypto).child("Data").child(currency).child("price").get().val()
                                old_timestamp = db.child(crypto).child("Data").child(currency).child("timestamp").get().val()
                                if old_price is not None:
                                    dict[crypto][currency]["price"] = float(old_price)
                                else:
                                    dict[crypto][currency]["price"] = float(data[crypto][currency]["PRICE"])

                                if old_timestamp is not None:
                                    dict[crypto][currency]["timestamp"] =  float(old_timestamp)
                                else:
                                    dict[crypto][currency]["timestamp"] = float(data[crypto][currency]["LASTUPDATE"])

                            else:

                                dict[crypto][currency]["price"] = float(data[crypto][currency]["PRICE"])
                                dict[crypto][currency]["timestamp"] = float(data[crypto][currency]["LASTUPDATE"])

                            if currency == "INR" and rate is not None:
                                    dict[crypto]["INR"]["change_24hrs_fiat"] = float(
                                        data[crypto]["USD"]["CHANGE24HOUR"]*rate)
                                    dict[crypto][currency]["change_24hrs_percent"] = float(
                                        data[crypto]["USD"]["CHANGEPCT24HOUR"])
                            else:
                                dict[crypto][currency]["change_24hrs_fiat"] = float(data[crypto][currency]["CHANGE24HOUR"])
                                dict[crypto][currency]["change_24hrs_percent"] = float(data[crypto][currency]["CHANGEPCT24HOUR"])

                            dict[crypto][currency]["vol_24hrs_coin"] = float(data[crypto][currency]["VOLUME24HOUR"])
                            dict[crypto][currency]["vol_24hrs_fiat"] = float(data[crypto][currency]["VOLUME24HOURTO"])
                            dict[crypto][currency]["high_24hrs"] = float(data[crypto][currency]["HIGH24HOUR"])
                            dict[crypto][currency]["low_24hrs"] = float(data[crypto][currency]["LOW24HOUR"])
                            dict[crypto][currency]["last_trade_volume"] = float(data[crypto][currency]["LASTVOLUME"])
                            dict[crypto][currency]["last_trade_market"] = data[crypto][currency]["LASTMARKET"]
                            dict[crypto][currency]["supply"] = float(data[crypto][currency]["SUPPLY"])
                            dict[crypto][currency]["marketcap"] = float(data[crypto][currency]["MKTCAP"])
                            if crypto == "BTC":
                                dict[crypto][currency]["markets"] = btc_markets[currency]
                            elif crypto == "ETH":
                                dict[crypto][currency]["markets"] = eth_markets[currency]
                            elif crypto == "LTC":
                                dict[crypto][currency]["markets"] = ltc_markets[currency]
                            elif crypto == "XRP":
                                dict[crypto][currency]["markets"] = xrp_markets[currency]
                            elif crypto == "BCH":
                                dict[crypto][currency]["markets"] = bch_markets[currency]
                            elif crypto == "OMG":
                                dict[crypto][currency]["markets"] = omg_markets[currency]
                            elif crypto == "REQ":
                                dict[crypto][currency]["markets"] = req_markets[currency]
                            elif crypto == "ZRX":
                                dict[crypto][currency]["markets"] = zrx_markets[currency]
                            elif crypto == "BAT":
                                dict[crypto][currency]["markets"] = bat_markets[currency]
                            elif crypto == "GNT":
                                dict[crypto][currency]["markets"] = gnt_markets[currency]
                            elif crypto == "AE":
                                dict[crypto][currency]["markets"] = ae_markets[currency]
                            elif crypto == "RPX":
                                dict[crypto][currency]["markets"] = rpx_markets[currency]
                            elif crypto == "DBC":
                                dict[crypto][currency]["markets"] = dbc_markets[currency]
                            elif crypto == "XMR":
                                dict[crypto][currency]["markets"] = xmr_markets[currency]
                            elif crypto == "DOGE":
                                dict[crypto][currency]["markets"] = doge_markets[currency]
                            elif crypto == "SIA":
                                dict[crypto][currency]["markets"] = sia_markets[currency]
                            elif crypto == "XLM":
                                dict[crypto][currency]["markets"] = xlm_markets[currency]
                            elif crypto == "NEO":
                                dict[crypto][currency]["markets"] = neo_markets[currency]
                            else:
                                dict[crypto][currency]["markets"] = {}

        for coin in dict.keys():
            data = {"Data": dict[coin]}
            title = coin
            db.child(title).update(data)

def get_list_of_coins_with_rank():
    all_data = db.child("coins").order_by_key().limit_to_last(1).get()
    for data in all_data.each():
        return data.val()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

get_current_crypto_price()


