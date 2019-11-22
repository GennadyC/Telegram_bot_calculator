#ifndef RECT_SFML
#define RECT_SFML

#include <SFML/Graphics.hpp>

class Rect
{

private:
	sf::RectangleShape rect;

public:
	Rect();

	~Rect();

	sf::RectangleShape getRect();

	sf::Vector2f getPositionRect();
};

#endif