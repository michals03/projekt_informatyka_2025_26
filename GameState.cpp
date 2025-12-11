#include "GameState.h"
#include <fstream>
#include <iostream>

void GameState::capture(const Paletka& paletka,const Pilka& pilka,const std::vector<Stone>& stones,int aktualnyWynik) {
	paddlePosition=sf::Vector2f(paletka.getX(),paletka.getY());
	ballPosition=sf::Vector2f(pilka.getX(),pilka.getY());
	ballVelocity=sf::Vector2f(pilka.getVx(),pilka.getVy());
	this->wynik=aktualnyWynik;
	blocks.clear();
	for(const auto& s : stones) {
		// zapis tylko klocków ktore istnieja
		if(!s.isDestroyed()) {
			blocks.push_back({s.getPosition().x,s.getPosition().y,s.getHP(),s.getMaxHP() });
		}
	}
	std::cout<<"Przechwycono stan gry. Punkty: "<<wynik<<std::endl;
}
// zapis danych do pliku tekstowego
bool GameState::saveToFile(const std::string& filename){
	std::ofstream file(filename);
	if(!file.is_open())return false;
	file<<"PALETKA "<<paddlePosition.x<<" "<<paddlePosition.y<<"\n";
	file<<"PILKA "<<ballPosition.x<< " "<<ballPosition.y<<" "<< ballVelocity.x<<" "<<ballVelocity.y<<"\n";
	file<<"WYNIK "<<wynik<<"\n";
	file<<"LICZBA_BLOKOW "<<blocks.size()<<"\n";
	for(const auto& b : blocks) {
		file<<b.x<<" "<<b.y<<" "<<b.hp<<" "<<b.maxHp<<"\n";
	}
	file.close();
	std::cout<<"Zapisano stan gry do pliku:"<<filename<<std::endl;
	return true;
}
// wczytanie danych z pliku tekstowego
bool GameState::loadFromFile(const std::string& filename) {
	std::ifstream file(filename);
	if(!file.is_open())return false;
	std::string label;
	if(!(file>>label>>paddlePosition.x>>paddlePosition.y))return false;
	if(!(file>>label>>ballPosition.x>>ballPosition.y>>ballVelocity.x>>ballVelocity.y))return false;
	if(!(file>>label>>wynik))return false;
	int count;
	if(!(file>>label>>count))return false;
	blocks.clear();
	for (int i=0;i<count;i++) {
		BlockData bd;
		file>>bd.x>>bd.y>>bd.hp>>bd.maxHp;
		blocks.push_back(bd);
	}
	file.close();
	std::cout<<"Wczytano gre z pliku. Punkty: "<<wynik<< std::endl;
	return true;
}
// przypisanie wczytanych danych do obiektow gry
void GameState::apply(Paletka& paletka,Pilka& pilka,std::vector<Stone>& stones,int& wynikRef) {
	paletka.setPosition(paddlePosition.x,paddlePosition.y);
	pilka.setPosition(ballPosition.x,ballPosition.y);
	pilka.setVelocity(ballVelocity.x,ballVelocity.y);
	wynikRef = wynik;
	stones.clear();
	const float ROZMIAR_BLOKU_X=(800.f-(8-1)*2.f)/8;
	const float ROZMIAR_BLOKU_Y=30.f;
	sf::Vector2f size(ROZMIAR_BLOKU_X,ROZMIAR_BLOKU_Y);
	for(const auto&data : blocks) {
		stones.emplace_back(sf::Vector2f(data.x,data.y),size,data.hp,data.maxHp);
	}
}