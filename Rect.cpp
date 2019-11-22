#include "Rect.h"

Rect::Rect()
{
	sf::RectangleShape rect(sf::Vector2f(100.f, 100.f));
	rect.setSize(sf::Vector2f(100.f, 100.f));
	rect.setFillColor(sf::Color::Red);
	rect.setPosition(sf::Vector2f(100.f, 100.f));
	this->rect = rect;
}

Rect::~Rect()
{

}


sf::RectangleShape Rect::getRect()
{
	return rect;
}

sf::Vector2f Rect::getPositionRect()
{
	return rect.getPosition();
}