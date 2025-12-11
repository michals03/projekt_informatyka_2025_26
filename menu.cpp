#include "Menu.h"
#include <iostream>

Menu::Menu(float width,float height)
{
	if(!font.loadFromFile("arial.ttf"))
	{
		std::cerr<<"Nie znaleziono czcionki arial.ttf!"<<std::endl;
		return;
	}
	std::string opcje[MAX_LICZBA_POZIOMOW]={"Nowa gra","Wczytaj gre","Ostatnie wyniki","Wyjscie"};
	for(int i=0;i<MAX_LICZBA_POZIOMOW;i++) {
		menu[i].setFont(font);
		menu[i].setString(opcje[i]);
		sf::FloatRect textRect=menu[i].getLocalBounds();
		menu[i].setOrigin(textRect.left+textRect.width/2.0f,textRect.top+textRect.height/2.0f);
		menu[i].setPosition(sf::Vector2f(width/2.0f,height/(MAX_LICZBA_POZIOMOW+1)*(i+1)));
		if(i==0) {
			menu[i].setFillColor(sf::Color::Cyan);
			menu[i].setStyle(sf::Text::Bold);
		}
		else{
			menu[i].setFillColor(sf::Color::White);
		}
	}
}
void Menu::draw(sf::RenderWindow& window)
{
	for(int i=0;i<MAX_LICZBA_POZIOMOW;i++)
		window.draw(menu[i]);
}
void Menu::przesunG()
{
	if(selectedItem-1>=0){
		menu[selectedItem].setFillColor(sf::Color::White);
		menu[selectedItem].setStyle(sf::Text::Regular);
		selectedItem--;
		menu[selectedItem].setFillColor(sf::Color::Cyan);
		menu[selectedItem].setStyle(sf::Text::Bold);
	}
	else{
		menu[selectedItem].setFillColor(sf::Color::White);
		menu[selectedItem].setStyle(sf::Text::Regular);
		selectedItem=MAX_LICZBA_POZIOMOW-1;
		menu[selectedItem].setFillColor(sf::Color::Cyan);
		menu[selectedItem].setStyle(sf::Text::Bold);
	}
}

void Menu::przesunD()
{
	if(selectedItem+1<MAX_LICZBA_POZIOMOW){
		menu[selectedItem].setFillColor(sf::Color::White);
		menu[selectedItem].setStyle(sf::Text::Regular);
		selectedItem++;
		menu[selectedItem].setFillColor(sf::Color::Cyan);
		menu[selectedItem].setStyle(sf::Text::Bold);
	}
	else{ 
		menu[selectedItem].setFillColor(sf::Color::White);
		menu[selectedItem].setStyle(sf::Text::Regular);
		selectedItem=0;
		menu[selectedItem].setFillColor(sf::Color::Cyan);
		menu[selectedItem].setStyle(sf::Text::Bold);
	}
}