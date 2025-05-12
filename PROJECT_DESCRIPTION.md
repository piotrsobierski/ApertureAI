# Mini-Projekt: Prosty Asystent Opisywania i Tagowania Zdjęć z FAQ w Chmurze

## Opis Problemu:

Chcemy stworzyć prostego asystenta, który będzie mógł opisywać zawartość przesłanych
zdjęć oraz przypisywać im tagi. Dodatkowo asystent powinien być w stanie odpowiadać na
proste pytania zdefiniowane w pliku FAQ.

## Cel Zadania:

Zaproponuj i zaimplementuj minimalny działający system do opisywania i tagowania zdjęć
oraz odpowiadania na pytania FAQ, wykorzystując modele językowe (LLM), gotowe
komponenty i podstawowe usługi chmurowe.

## Wymagania:

**Wybór Technologii Chmurowych i Gotowych Komponentów:**

- Wybierz jedną platformę chmurową (AWS, Azure lub GCP) i uzasadnij swój
  wybór.
- Wskaż, jakie konkretne gotowe komponenty lub usługi chmurowe (np. API do
  analizy obrazu, API LLM, bazy danych) zamierzasz wykorzystać do analizy
  zdjęć i przetwarzania tekstu FAQ.

**Integracja z LLM i API Obrazu:**

- Wykorzystaj publicznie dostępne API LLM (np. OpenAI API) do generowania
  opisów i tagów na podstawie analizy obrazu oraz do odpowiadania na pytania
  z FAQ.
- Opisz, jak będziesz przekazywać obrazy do API analizy obrazu i jak
  przetworzysz wynikową analizę, aby wygenerować opis i tagi za pomocą LLM
  (wybór technologii dowolny).
- Opisz, jak zintegrujesz LLM z plikiem FAQ, aby odpowiadać na pytania
  użytkownika. Możesz rozważyć proste dopasowanie zapytań do istniejących
  pytań i odpowiedzi w FAQ lub bardziej zaawansowane techniki (np.
  embeddingi).

**Prosty Interfejs Użytkownika (Opcjonalnie, ale mile widziane):**

- Jeśli czas pozwoli, stwórz bardzo prosty interfejs (np. w Pythonie z
  streamlit, prosty skrypt interaktywny w terminalu lub endoint api), który
  pozwoli użytkownikowi przesłać zdjęcie i zadać pytanie (ogólne lub dotyczące
  FAQ) oraz wyświetli wygenerowany opis, tagi i odpowiedź.

**Opis Rozwiązania:**

- Przygotuj krótki opis (maks. 1 strona), w którym wyjaśnisz, jakie usługi
  chmurowe i gotowe komponenty zostały użyte, jak zintegrowane są
  komponenty oraz jakie są ograniczenia Twojego rozwiązania.

## Kryteria Oceny:

- Zrozumienie problemu i trafność prostego rozwiązania.
- Świadome wykorzystanie gotowych komponentów i API chmurowych i/lub LLM
  do analizy obrazu i przetwarzania tekstu.
- Poprawna integracja LLM z wynikami analizy obrazu i danymi FAQ.
- Logiczność przepływu informacji.
- Jasność opisu rozwiązania.

## Instrukcje dla Kandydata:

- Prosimy o przesłanie opisu rozwiązania oraz ewentualnego kodu.
- Będziemy chcieli usłyszeć od Ciebie, jak wyobrażasz sobie dalszy rozwój tego
  prostego asystenta w bardziej zaawansowany system w chmurze, uwzględniając
  skalowalność i obsługę większej ilości funkcji.
- dodatkowym atutem będzie wystawienie gotowego rozwiązania do testów.
- w razie pytań i wątpliwości proszę pisać na jkulesza@grupazpr.pl
