# KPI aprēķins: Izmaksas un marža
# Uzdevums: ievadi datus par vairākiem produktiem un apskatī rezultātus

# -------------------------------------------------------
# 1. DATU IEVADE
# Ievāc datus par vairākiem produktiem un glabā tos sarakstos (list)
# -------------------------------------------------------

produkti = []
ienemumi = []
izmaksas = []

skaits = int(input("Cik produktus vēlies ievadīt? "))

for i in range(skaits):
    print(f"\n--- Produkts {i + 1} ---")
    nosaukums = input("Produkta nosaukums: ")
    # TODO: ievāc ieņēmumus un izmaksas (izmanto float() konvertācijai)

# -------------------------------------------------------
# 2. APRĒĶINI
# Izmanto for ciklu, lai aprēķinātu katram produktam:
#   - peļņu (ieņēmumi - izmaksas)
#   - bruto maržu % ( peļņa / ieņēmumi * 100 )
# -------------------------------------------------------

rezultati = {}  # vārdnīca: produkta nosaukums -> {pelna, marzas_procents}

for i in range(skaits):
    # TODO: aprēķini peļņu un maržu
    pass

# -------------------------------------------------------
# 3. LĒMUMU LOĢIKA
# Izmanto if/elif/else, lai katram produktam izvērtētu maržu:
#   > 50% — "Lieliska marža"
#   20–50% — "Laba marža"
#   < 20% — "Zema marža, pārskati izmaksas"
# -------------------------------------------------------

print("\n===== KPI PĀRSKATS =====")

for nosaukums, dati in rezultati.items():
    # TODO: izvadi rezultātus un pievieno if/elif/else vērtējumu
    pass

# -------------------------------------------------------
# 4. KOPSAVILKUMS
# TODO: aprēķini un izvadi:
#   - kopējos ieņēmumus (sum())
#   - kopējās izmaksas (sum())
#   - kopējo peļņu
#   - vidējo maržu visos produktos
# -------------------------------------------------------
