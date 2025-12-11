#pragma once
#include <SFML/Graphics.hpp>
class Paletka {
private:
	float x, y;
	float szerokosc, wysokosc;
	float predkosc;
	sf::RectangleShape shape;
public:
	Paletka(float startX,float startY,float szerokosc,float wysokosc,float predkosc)
		:x(startX),y(startY),szerokosc(szerokosc),wysokosc(wysokosc),predkosc(predkosc) {
		shape.setSize({szerokosc,wysokosc});
		shape.setOrigin(szerokosc/2,wysokosc/2);
		shape.setPosition(x,y);
		shape.setFillColor(sf::Color::Red);
	}
	void moveLeft() {
		x-=predkosc;
		shape.setPosition(x,y);
	}
	void moveRight() {
		x+=predkosc;
		shape.setPosition(x,y);
	}
	// zatrzymuje paletke na krawedziach ekranu
	void clampToBounds(float width) {
		if(x-szerokosc/2<0)x=szerokosc/2;
		else if(x+szerokosc/2>width)x=width-szerokosc/2;
		shape.setPosition(x,y);
	}
	void setPosition(float newX,float newY) {
		x=newX;
		y=newY;
		shape.setPosition(x,y);
	}
	sf::FloatRect getGlobalBounds()const {
		return shape.getGlobalBounds();
	}
	void draw(sf::RenderTarget& target) {
		target.draw(shape);
	}
	float getX()const{return x;}
	float getY()const{return y;}
	float getSzerokosc()const{return szerokosc;}
	float getWysokosc()const{return wysokosc;}
};