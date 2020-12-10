import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

"""Dane wejściowe i zmienne symulacji tutaj"""
Kasy = 5

V_k = 0.5 # pół koszyka na minutę

cashier_flag = 1

"""Wejścia symulacji"""

env = simpy.RealtimeEnvironment()

seller_line1 = simpy.Resource(env, capacity = cashier_flag)
seller_line2 = simpy.Resource(env, capacity = cashier_flag)
seller_line3 = simpy.Resource(env, capacity = cashier_flag)
seller_line4 = simpy.Resource(env, capacity = cashier_flag)
seller_line5 = simpy.Resource(env, capacity = cashier_flag)

sellers_lines = []

sellers_lines.append(seller_line1)
sellers_lines.append(seller_line2)
sellers_lines.append(seller_line3)
sellers_lines.append(seller_line4)
sellers_lines.append(seller_line5)

czasy = []

"""Symulacja odbywa się tutaj """

def Kolejka(seller_lines, env,nazwa, V, seller_flag):
    global czasy
    """W tej funkcji odbywa się symulacja kolejki,

       parametry wejściowe :

           seller_lines - kasy w sklepie (in : lista)

           env - Symulacja (in : evironment z simpy)

           nazwa - parametr podający nazwę itego klienta ( in: var)

           V - prędkości obsługi w koszykach na minutę (in : float )

           seller_flag - przy ilu osobach w kolejce uruchamiamy następną kasę (in : int)

       parametry wyjściowe :

            Przebieg symulacji



       Ważne! do zrobienia jeszcze

            dodać czas otwierania kasy

            dodać wyjściowe rzeczy do badania (czas itp)

            i w sumie niewiem


       """



    #podejście do kas

    yield env.timeout(random.uniform(0.1, 0.5)) #!!!!!
    czas_start = env.now
    print('%s Szuka wolnej kasy o czasie :  %d' % (nazwa, env.now))

    # sprawdzenie czy jakaś kasa wolna jak tak to podchodzi

    customer_line1 = seller_lines[0]
    customer_line2 = seller_lines[1]
    customer_line3 = seller_lines[2]
    customer_line4 = seller_lines[3]
    customer_line5 = seller_lines[4]

    #kalkulowanie kolejki do kasy 1
    customer_at_this_moment_1 = customer_line1.queue
    customer_at_this_moment_1 = len(customer_at_this_moment_1)

    #kalkulowanie kolejki do kasy 2
    customer_at_this_moment_2 = customer_line2.queue
    customer_at_this_moment_2 = len(customer_at_this_moment_2)

    #kalkulowanie kolejki do kasy 3
    customer_at_this_moment_3 = customer_line3.queue
    customer_at_this_moment_3 = len(customer_at_this_moment_3)

    # kalkulowanie kolejki do kasy 4

    customer_at_this_moment_4 = customer_line4.queue
    customer_at_this_moment_4 = len(customer_at_this_moment_4)

    #kalkulowanie kolejki do kasy 5

    customer_at_this_moment_5 = customer_line5.queue
    customer_at_this_moment_5 = len(customer_at_this_moment_5)


    print('Kolejka do kasy 1 : ',customer_at_this_moment_1)
    print('Kolejka do kasy 2 : ', customer_at_this_moment_2)
    print('Kolejka do kasy 3 : ', customer_at_this_moment_3)
    print('Kolejka do kasy 4 : ', customer_at_this_moment_4)
    print('Kolejka do kasy 5 : ', customer_at_this_moment_5)

    # Klient patrzy na 1 kase
    if customer_at_this_moment_1 < seller_flag :
        #kasa wolna może podchodzić
        with customer_line1.request() as rq:

            yield rq

            basket_size = random.uniform(0.1, 2)
            czas_kasowania = basket_size / V

            #rozpoczyna się kasować
            print('%s zaczyna kasować w kasie 1 o czasie %d' % (nazwa, env.now))
            yield env.timeout(czas_kasowania)
            print('%s odchodzi od kasy 1 o czasie  %d' % (nazwa, env.now))
            czas_koniec = env.now


    elif customer_at_this_moment_1 >= seller_flag:
        # kasa 1 zajęta, podchodzi do 2

        if customer_at_this_moment_2 < seller_flag:

            #kasa 2 wolna, stoi w kolejce
            with customer_line2.request() as rq1:
                yield rq1

                basket_size = random.uniform(0.1, 2)
                czas_kasowania = basket_size / V

                # rozpoczyna się kasować
                print('%s zaczyna kasować w kasie 2 o czasie %d' % (nazwa, env.now))
                yield env.timeout(czas_kasowania)
                print('%s odchodzi od kasy 2 o czasie %d' % (nazwa, env.now))
                czas_koniec = env.now

        elif customer_at_this_moment_2 >=seller_flag:

            # kasa zajęta idzie do 3

            if customer_at_this_moment_3 < seller_flag:

                # kasa 3 wolna, stoi w kolejce i kasuje

                with customer_line3.request() as rq2:
                    yield rq2

                    basket_size = random.uniform(0.1, 2)
                    czas_kasowania = basket_size / V

                    # rozpoczyna się kasować
                    print('%s zaczyna kasować w kasie 3 o czasie   %d' % (nazwa, env.now))
                    yield env.timeout(czas_kasowania)
                    print('%s odchodzi od kasy 3 o czasie %d' % (nazwa, env.now))
                    czas_koniec = env.now

            elif customer_at_this_moment_3 >= seller_flag:

                # kasa 3 zajęta idzie do 4

                if customer_at_this_moment_4 < seller_flag:

                    # kasa 4 wolna, zaczyna kasować

                    with customer_line4.request() as rq3:
                        yield rq3

                        basket_size = random.uniform(0.1, 2)
                        czas_kasowania = basket_size / V

                        # rozpoczyna się kasować
                        print('%s zaczyna kasować w kasie 4 o czasie  %d' % (nazwa, env.now))
                        yield env.timeout(czas_kasowania)
                        print('%s odchodzi od kasy 4 o czasie %d' % (nazwa, env.now))
                        czas_koniec = env.now

                elif customer_at_this_moment_4 >= seller_flag:
                    # kasa 4 zajęta, idzie do 5

                    if customer_at_this_moment_5 < seller_flag:

                        #kasa 5 wolna, zaczyna kasowac

                        with customer_line5.request() as rq4:
                            yield rq4

                            basket_size = random.uniform(0.1, 2)
                            czas_kasowania = basket_size / V

                            # rozpoczyna się kasować
                            print('%s zaczyna kasować w kasie 5  %d' % (nazwa, env.now))
                            yield env.timeout(czas_kasowania)
                            print('%s odchodzi od kasy 5 o czasie %d' % (nazwa, env.now))
                            czas_koniec = env.now

                    elif customer_at_this_moment_5 >= seller_flag:
                        # tutaj mamy szczególny przypadek gdy wszystkie kasy są zajęte i mamy nadal przypływ ludzi
                        # mój pomysł to po prostu z randoma wybrać kasę do której podejdzie jeszcze nie wiem jak to do
                        # końca napisać bo mi błędy wyskakują
                        x = [customer_at_this_moment_1, customer_at_this_moment_2, customer_at_this_moment_3,
                                 customer_at_this_moment_4, customer_at_this_moment_5]
                        shortest_queue = min(x)
                        id = x.index(shortest_queue)

                        with sellers_lines[id].request() as rq5:
                            yield rq5

                            basket_size = random.uniform(0.1, 2)
                            czas_kasowania = basket_size / V

                            # rozpoczyna się kasować
                            print('%s zaczyna kasować w kasie 5  %d' % (nazwa, env.now))
                            yield env.timeout(czas_kasowania)
                            print('%s odchodzi od kasy 5 o czasie %d' % (nazwa, env.now))
                            czas_koniec = env.now


    czas_roznica = czas_koniec - czas_start
    czasy.append(czas_roznica)
    print('%s Spedzil w sklepie czasu tyle :  %d' % (nazwa, czas_roznica))




""" RUN  """
def next_client(env):
    client_id = 1
    while True:
        yield env.timeout(random.uniform(0.3, 0.9))
        env.process(Kolejka(sellers_lines, env, 'Klient %d ' % client_id, V_k, 4))
        client_id = client_id + 1

env.process(next_client(env))
env.run(until= 400)
print("!!! SYMULACJA ZAKONCZONA !!!")
print("Tablicza czasów:\n",czasy,"\n")
print("Srednia przebywania klienta w systemie:", np.mean(czasy))

plt.plot(czasy)
plt.show()