#pragma once
#include <SFML/Graphics.hpp>
#include "paletka.h"
#include <cmath>
class Pilka {
private:
	float x,y;
	float vx,vy; 
	float promien;
	sf::CircleShape shape;
public:
	Pilka(float startX,float startY,float vx,float vy,float promien)
		:x(startX),y(startY),vx(vx),vy(vy),promien(promien) {
		shape.setRadius(promien);
		shape.setOrigin(promien,promien);
		shape.setPosition(x,y);
		shape.setFillColor(sf::Color::White);
	}
	void move() {
		x += vx;
		y += vy;
		shape.setPosition(x,y);
	}
	void bounceX() {vx= -vx;}
	void bounceY() {vy= -vy;}
	// sprawdza i obsluguje odbicia od scian
	void collideWalls(float width,float height) {
		if(x-promien<= 0||x+promien>=width) {
			bounceX();
			if(x-promien<=0)x=promien;
			if(x+promien>=width)x=width-promien;
		}
		if(y-promien<=0) {
			bounceY();
			y=promien;
		}
	}
	// kolizja z paletka
	bool collidePaddle(const Paletka&p) {
		// sprawdzenie czy pilka jest w obrebie paletki
		if(x>=p.getX()-p.getSzerokosc()/2 && x<=p.getX()+p.getSzerokosc()/2 && (y+promien)>=(p.getY()-p.getWysokosc()/2) && (y-promien)<(p.getY()-p.getWysokosc()/2)) {
			vy= -std::abs(vy); 
			y=p.getY()-p.getWysokosc()/2-promien;
			return true;
		}
		return false;
	}
	void setPosition(float newX,float newY) {
		x=newX;
		y=newY;
		shape.setPosition(x,y);
	}
	void setVelocity(float newVx,float newVy) {
		vx=newVx;
		vy=newVy;
	}
	void draw(sf::RenderTarget& target) {target.draw(shape);}
	float getX()const{return x;}
	float getY()const{return y;}
	float getVx()const{return vx;}
	float getVy()const{return vy;}
	float getRadius()const{return promien;}
};