#include <SFML/Graphics.hpp>
#include <iostream>
#include <ctime>
#include <cstdlib>
#include "Menu.h"
#include "Game.h"
#include "wyniki.h"

enum class AppState { Menu, Playing, Scores, Exiting };
int main() {

	std::srand(static_cast<unsigned int>(std::time(NULL)));
	sf::RenderWindow window(sf::VideoMode(800,600),"Arkanoid");
	window.setFramerateLimit(60);
	Menu menu(window.getSize().x,window.getSize().y);
	Game game;
	MenedzerWynikow menedzerWynikow("lista_wynikow.txt");
	sf::Clock dtClock;
	AppState currentState=AppState::Menu;
	
	sf::Font font;
	if (!font.loadFromFile("arial.ttf")) {
		std::cerr<<"Blad ladowania czcionki"<<std::endl;
		return -1;
	}
	sf::Text titleText;
	titleText.setFont(font);
	titleText.setString("NAJLEPSZE WYNIKI");
	titleText.setCharacterSize(40);
	titleText.setFillColor(sf::Color::Yellow);
	titleText.setPosition(200,50);
	sf::Text scoresListText;
	scoresListText.setFont(font);
	scoresListText.setCharacterSize(30);
	scoresListText.setFillColor(sf::Color::White);
	scoresListText.setPosition(250,150);
	sf::Text congratsText;
	congratsText.setFont(font);
	congratsText.setString("GRATULACJE! WYGRALES!");
	congratsText.setCharacterSize(50);
	congratsText.setFillColor(sf::Color::Green);
	sf::FloatRect textRect=congratsText.getLocalBounds();
	congratsText.setOrigin(textRect.left+textRect.width/2.0f,textRect.top+textRect.height/2.0f);
	congratsText.setPosition(400,300);

	while(window.isOpen()){
		sf::Time dt=dtClock.restart();
		sf::Event event;
		while (window.pollEvent(event)) {
			if(event.type==sf::Event::Closed)window.close();
			if(currentState==AppState::Menu) {
				if(event.type==sf::Event::KeyPressed) {
					if(event.key.code==sf::Keyboard::Up) {
						menu.przesunG();
					}
					if(event.key.code==sf::Keyboard::Down) {
						menu.przesunD();
					}
					if(event.key.code==sf::Keyboard::Enter) {
						int wybrano=menu.getSelectedItem();
						if(wybrano==0) {
							game.reset();
							currentState=AppState::Playing;
						}
						else if(wybrano==1) {
							if(game.loadGame("zapisgry.txt")) {
								currentState = AppState::Playing;
							}
							else{
								std::cout << "Brak zapisanej gry\n";
							}
						}
						else if(wybrano==2) {
							std::vector<int>wyniki=menedzerWynikow.pobierzNajlepszeWyniki();
							std::string listStr="";
							for(size_t i=0;i<wyniki.size();i++) {
								listStr+=std::to_string(i+1)+". "+std::to_string(wyniki[i])+" pkt\n";
							}
							if(wyniki.empty())listStr="Brak zapisanych wynikow.";
							scoresListText.setString(listStr);
							currentState=AppState::Scores;
						}
						else if(wybrano==3) {
							currentState=AppState::Exiting;
						}
					}
				}
			}
			else if(currentState==AppState::Playing||currentState==AppState::Scores) {
				if(event.type==sf::Event::KeyPressed&&event.key.code==sf::Keyboard::Escape)
					currentState=AppState::Menu;
			}
		}
		if (currentState==AppState::Exiting)window.close();
		else if(currentState==AppState::Playing) {
			if(game.update(dt)==false) {
				menedzerWynikow.zapiszWynik(game.getWynik());
				if(game.isVictory()) {
					window.clear(sf::Color::Black);
					window.draw(congratsText);
					window.display();
					sf::sleep(sf::seconds(3));
				}
				else{
					std::cout<<"KONIEC GRY\n";
				}
				currentState=AppState::Menu;
			}
		}
		window.clear(sf::Color::Black);
		if(currentState==AppState::Menu) {
			menu.draw(window);
		}
		else if(currentState==AppState::Playing) {
			game.render(window);
		}
		else if(currentState==AppState::Scores) {
			window.draw(titleText);
			window.draw(scoresListText);
		}
		window.display();
	}
	return 0;
}