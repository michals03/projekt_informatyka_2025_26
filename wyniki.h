#pragma once
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <iostream>
class MenedzerWynikow {
private:
	std::string nazwaPliku;
public:
	MenedzerWynikow(const std::string& plik) :nazwaPliku(plik) {}
	// zapis nowego wyniku
	void zapiszWynik(int wynik) {
		std::vector<int>wyniki=pobierzNajlepszeWyniki();
		wyniki.push_back(wynik);
		std::sort(wyniki.rbegin(),wyniki.rend()); // sortowanie malejaco
		if(wyniki.size()>5) {
			wyniki.resize(5); // zapis tylko top 5
		}
		std::ofstream plikWyjsciowy(nazwaPliku);
		if(plikWyjsciowy.is_open()) {
			for(int w:wyniki) {
				plikWyjsciowy<<w<<"\n";
			}
		}
	}
	// odczyt wyników z pliku
	std::vector<int>pobierzNajlepszeWyniki() {
		std::vector<int>wyniki;
		std::ifstream plikWejsciowy(nazwaPliku);
		int wartosc;
		if(plikWejsciowy.is_open()) {
			while(plikWejsciowy>>wartosc) {
				wyniki.push_back(wartosc);
			}
		}
		std::sort(wyniki.rbegin(),wyniki.rend());
		return wyniki;
	}
};