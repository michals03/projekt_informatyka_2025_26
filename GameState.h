#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>
#include "kostka.h"
#include "paletka.h"
#include "pilka.h"

struct BlockData {
	float x,y;
	int hp;
	int maxHp;
};

class GameState {
private:
	sf::Vector2f paddlePosition;
	sf::Vector2f ballPosition;
	sf::Vector2f ballVelocity;
	std::vector<BlockData>blocks;
	int wynik;
public:
	void capture(const Paletka& paletka,const Pilka& pilka,const std::vector<Stone>& stones,int aktualnyWynik);
	bool saveToFile(const std::string& filename);
	bool loadFromFile(const std::string& filename);
	void apply(Paletka& paletka,Pilka& pilka,std::vector<Stone>& stones,int& wynikRef);
};