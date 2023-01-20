database = {'crops' :
    [
        {"maiz": [
                {
                    24 : 1.2,
                    25 : 1.4,
                    26 : 1.3,
                    27 : 1,
                    28 : 0.5
                }
            ],
        },
        {"banano": [
                {
                    24 : 45,
                    25 : 50,
                    26 : 47,
                    27 : 45,
                    28 : 40,
                    29 : 33,
                    30 : 25
                }
            ],
        },
        {"arroz": [
                {
                    24 : 2.2,
                    25 : 2.7,
                    26 : 2.5,
                    27 : 1.5,
                    28 : 0.5
                }
            ],
        },
    ]
}
def get_profitability(temperature, crop):
    val = 0
    if crop == 'maiz':
        val = 0
    elif crop == 'banano':
        val = 1
    elif crop == 'arroz':
        val = 2
    print(val)
    bestValue = 1
    #Change crop static value for dinamic variable crop
    nearestNum = min(database['crops'][val][crop][0], key=lambda x: abs(x - temperature))
    #print(database['crops'][0]['maiz'][0][nearestNum])
    bestValue = database['crops'][val][crop][0][25]
    return database['crops'][val][crop][0][nearestNum], bestValue

#print(database['crops'][1])
#print(get_profitability(25.6, 'arroz'))