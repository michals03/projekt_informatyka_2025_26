#pragma once
#include <SFML/Graphics.hpp>
#include <vector>
#include <string>
#include "paletka.h"
#include "pilka.h"
#include "kostka.h"
#include "GameState.h"

struct Bonus {
	sf::ConvexShape shape;
	bool active;
	float speed;
};

class Game {
private:
	Paletka paletka;
	Pilka pilka;
	std::vector<Stone>bloki;
	bool isPaused;
	sf::Font font;
	sf::Text wynikText;
	int wynik;
	Bonus bonus;
	bool victory;
	void updateWynikText();
	sf::Text pauseText;      
	sf::Clock resumeClock;   
	bool showResumeMessage;  
public:
	Game();

	bool update(sf::Time dt);
	void render(sf::RenderTarget& target);
	void reset();
	void saveGame(const std::string& filename);
	bool loadGame(const std::string& filename);
	int getWynik()const {return wynik;}
	void setWynik(int s) {wynik=s;updateWynikText();}
	bool isVictory()const {return victory;}
};