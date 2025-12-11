#pragma once
#include <SFML/Graphics.hpp>
#include <array>
class Stone :public sf::RectangleShape {
private:
	int m_punktyZycia; 
	int m_maxHP;
	bool m_jestZniszczony;
	static const std::array<sf::Color,4>m_colorLUT;
public:
	Stone(sf::Vector2f startPos,sf::Vector2f rozmiar,int hp,int customMaxHP=0)
		:m_punktyZycia(hp),m_jestZniszczony(false) {
		if(customMaxHP>0) {
			m_maxHP=customMaxHP;
		}
		else{
			m_maxHP=hp;
		}
		this->setPosition(startPos);
		this->setSize(rozmiar);
		this->setOutlineThickness(2.f);
		this->setOutlineColor(sf::Color(0,0,0));
		aktualizujKolor();
	}
	void trafienie() {
		if(m_jestZniszczony)return;
		m_punktyZycia--;
		aktualizujKolor();
		if(m_punktyZycia<=0) {
			m_jestZniszczony=true;
		}
	}
	void aktualizujKolor() {
		if(m_punktyZycia>=0&&m_punktyZycia<(int)m_colorLUT.size()) {
			this->setFillColor(m_colorLUT[m_punktyZycia]);
		}
		else if(m_punktyZycia>0) {
			this->setFillColor(m_colorLUT.back());
		}
		else{
			this->setFillColor(m_colorLUT.front());
		}
	}
	bool isDestroyed()const {return m_jestZniszczony;}
	int getHP()const {return m_punktyZycia;}
	int getMaxHP()const {return m_maxHP;}
	int getPointsValue()const{
		return m_maxHP*10;
	}
	void draw(sf::RenderTarget& target)const{
		if(!m_jestZniszczony) {
			target.draw(*this);
		}
	}
};