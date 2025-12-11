#include "Game.h"
#include <iostream>
#include <cstdlib>

const std::array<sf::Color,4>Stone::m_colorLUT={sf::Color::Transparent,sf::Color::Green,sf::Color::White,sf::Color::Blue};
// ustawianie stanu poczatkowego
Game::Game():paletka(400.f,550.f,100.f,20.f,8.f),pilka(400.f,300.f,4.f,3.f,8.f),isPaused(false),wynik(0),victory(false)
{
	// konfiguracja bonusu
	bonus.active = false;
	bonus.speed = 3.0f;
	bonus.shape.setPointCount(10);
	bonus.shape.setPoint(0,sf::Vector2f(15.f,0.f));
	bonus.shape.setPoint(1,sf::Vector2f(18.f,12.f));
	bonus.shape.setPoint(2,sf::Vector2f(30.f,12.f));
	bonus.shape.setPoint(3,sf::Vector2f(21.f,20.f));
	bonus.shape.setPoint(4,sf::Vector2f(24.f,30.f));
	bonus.shape.setPoint(5,sf::Vector2f(15.f,24.f));
	bonus.shape.setPoint(6,sf::Vector2f(6.f,30.f));
	bonus.shape.setPoint(7,sf::Vector2f(9.f,20.f));
	bonus.shape.setPoint(8,sf::Vector2f(0.f,12.f));
	bonus.shape.setPoint(9,sf::Vector2f(12.f,12.f));
	bonus.shape.setFillColor(sf::Color(255,215,0));
	bonus.shape.setOrigin(15.f,15.f);

	if(!font.loadFromFile("arial.ttf")) {
		std::cerr<<"Nie udalo sie wczytac czcionki"<<std::endl;
	}
	wynikText.setFont(font);
	wynikText.setCharacterSize(24);
	wynikText.setFillColor(sf::Color::White);
	wynikText.setPosition(10.f,565.f);

	pauseText.setFont(font);
	pauseText.setCharacterSize(30);
	pauseText.setFillColor(sf::Color::Yellow);
	pauseText.setOutlineColor(sf::Color::Black);
	pauseText.setOutlineThickness(3.f);
	showResumeMessage=false;

	reset();
}
// update punktow na ekranie
void Game::updateWynikText() {
	wynikText.setString("Punkty: "+std::to_string(wynik));
}
// nowa gra
void Game::reset(){
	paletka=Paletka(400.f,550.f,100.f,20.f,8.f);
	pilka=Pilka(400.f,300.f,4.f,3.f,8.f);
	isPaused=false;
	wynik=0;
	victory=false;
	bonus.active=false;
	bonus.shape.setRotation(0.f);
	updateWynikText();
	bloki.clear();
	const int ILOSC_KOLUMN=8;
	const int ILOSC_WIERSZY=7;
	const float ROZMIAR_BLOKU_Y=30.f;
	const float ROZMIAR_BLOKU_X=(800.f-(ILOSC_KOLUMN-1)*2.f)/ILOSC_KOLUMN;
	for(int y=0;y<ILOSC_WIERSZY;y++){
		for(int x=0; x<ILOSC_KOLUMN;x++){
			float pozX=(ROZMIAR_BLOKU_X+2.f)*x;
			float pozY=(ROZMIAR_BLOKU_Y+2.f)*y;
			int hp=(y<1)?3 : (y<3)?2 : 1;
			bloki.emplace_back(sf::Vector2f(pozX,pozY),sf::Vector2f(ROZMIAR_BLOKU_X,ROZMIAR_BLOKU_Y),hp);
		}
	}
}
void Game::saveGame(const std::string& filename){
	GameState state;
	state.capture(paletka,pilka,bloki,wynik);
	state.saveToFile(filename);
}

bool Game::loadGame(const std::string&filename) {
	GameState state;
	if(state.loadFromFile(filename)) {
		state.apply(paletka,pilka,bloki,wynik);
		isPaused=false;
		updateWynikText();
		bonus.active=false;
		victory=false;
		return true;
	}
	return false;
}

bool Game::update(sf::Time dt){
	if(sf::Keyboard::isKeyPressed(sf::Keyboard::P)){
		isPaused=!isPaused;

		if(isPaused){
			// napis na GRA WSTRZYMANA po wcisnieciu P
			pauseText.setString("GRA WSTRZYMANA");
			pauseText.setFillColor(sf::Color::Red);
			sf::FloatRect textRect=pauseText.getLocalBounds();
			pauseText.setOrigin(textRect.left+textRect.width/2.0f,textRect.top+textRect.height/2.0f);
			pauseText.setPosition(400.f,300.f);
			showResumeMessage=false;
		}
		else{
			//  napis WZNOWIONO GRE po kolejnym wcisnieciu P
			pauseText.setString("WZNOWIONO GRE");
			pauseText.setFillColor(sf::Color::Green);
			sf::FloatRect textRect=pauseText.getLocalBounds();
			pauseText.setOrigin(textRect.left+textRect.width/2.0f,textRect.top+textRect.height/2.0f);
			pauseText.setPosition(400.f,300.f);

			showResumeMessage=true;
			resumeClock.restart();
		}
		sf::sleep(sf::milliseconds(200));
	}
	if(isPaused)return true;

	if(showResumeMessage && resumeClock.getElapsedTime().asSeconds()>1.f) {
		showResumeMessage=false;
	}
	// zapis pod K
	if(sf::Keyboard::isKeyPressed(sf::Keyboard::K)) {
		saveGame("zapisgry.txt");
		sf::sleep(sf::milliseconds(200));
	}
	if(sf::Keyboard::isKeyPressed(sf::Keyboard::A)||sf::Keyboard::isKeyPressed(sf::Keyboard::Left))paletka.moveLeft();
	if(sf::Keyboard::isKeyPressed(sf::Keyboard::D)||sf::Keyboard::isKeyPressed(sf::Keyboard::Right))paletka.moveRight();
	paletka.clampToBounds(800.f);
	pilka.move();
	pilka.collideWalls(800.f, 600.f);
	if(pilka.collidePaddle(paletka)) {}
	if(bonus.active) {
		bonus.shape.move(0.f,bonus.speed);
		bonus.shape.rotate(2.f);
		if(bonus.shape.getPosition().y>600.f){
			bonus.active=false;
		}
		if(bonus.shape.getGlobalBounds().intersects(paletka.getGlobalBounds())) {
			wynik+=50;
			updateWynikText();
			bonus.active=false;
		}
	}
	int activeBlocks=0;
	for(auto& blok : bloki) {
		if(!blok.isDestroyed()) {
			activeBlocks++;
			sf::FloatRect pilkaBounds(pilka.getX()-pilka.getRadius(),pilka.getY()-pilka.getRadius(),pilka.getRadius()*2,pilka.getRadius()*2);
			if(pilkaBounds.intersects(blok.getGlobalBounds())) {
				blok.trafienie(); 
				if(blok.isDestroyed()) {
					wynik+=blok.getPointsValue();
					updateWynikText();
					activeBlocks--;
					if(!bonus.active&&(rand()%5==0)) {
						bonus.active=true;
						bonus.shape.setRotation(0.f);
						bonus.shape.setPosition(blok.getPosition().x+blok.getSize().x/2,blok.getPosition().y);
					}
				}
				float blokG=blok.getGlobalBounds().top;
				float blokD=blokG+blok.getGlobalBounds().height;
				if(pilka.getVy()>0&&(pilka.getY()+pilka.getRadius())<blokG+10.f)pilka.bounceY();
				else if(pilka.getVy()<0&&(pilka.getY()-pilka.getRadius())>blokD-10.f)pilka.bounceY();
				else pilka.bounceX();
				break;
			}
		}
	}
	if(activeBlocks==0) {
		std::cout<< "WYGRANA! WSZYSTKIE BLOKI ZNISZCZONE.\n";
		victory=true;
		wynik+=1000;
		return false;
	}
	if(pilka.getY()-pilka.getRadius()>600.f) {
		return false; 
	}
	if(sf::Keyboard::isKeyPressed(sf::Keyboard::P)) {
		isPaused=!isPaused;
		sf::sleep(sf::milliseconds(200));
	}
	return true; 
}
void Game::render(sf::RenderTarget& target) {
	paletka.draw(target);
	pilka.draw(target);
	for(const auto& blok : bloki)blok.draw(target);
	if(bonus.active) {
		target.draw(bonus.shape);
	}
	target.draw(wynikText);
	if(isPaused || showResumeMessage) {
		target.draw(pauseText);
	}
}