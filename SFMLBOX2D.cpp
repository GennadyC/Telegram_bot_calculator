#include <SFML/Graphics.hpp>
#include <iostream>
#include "Rect.h"


class Player
{

private:
	sf::CircleShape a;
	float coordX;
	float coordY;
	float speed = 0.1;
	bool borderLeft = false;
	bool borderRight = false;
	bool borderUp = false;
	bool borderDown = false;

public:
	Player()
	{
		sf::CircleShape shape(20.f);
		shape.setFillColor(sf::Color::Green);
		a = shape;
	}

	~Player()
	{

	}

	sf::CircleShape getShape()
	{
		return a;
	}

	void setBorderLeft(bool status)
	{
		borderLeft = status;
	}
	void setBorderRight(bool status)
	{
		borderRight = status;
		std::cout << borderUp << std::endl;
	}
	void setBorderUp(bool status)
	{
		borderUp = status;
	}
	void setBorderDown (bool status)
	{
		borderDown = status;
	}

	void Move()
	{
		if (sf::Keyboard::isKeyPressed(sf::Keyboard::A) && !borderLeft)
		{
			a.setPosition(sf::Vector2f(a.getPosition().x - speed, a.getPosition().y));
		}

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::D) && !borderRight)
		{
			a.setPosition(sf::Vector2f(a.getPosition().x + speed, a.getPosition().y));
			
		}

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::W) && !borderUp)
		{
			a.setPosition(sf::Vector2f(a.getPosition().x, a.getPosition().y - speed));
		}

		if (sf::Keyboard::isKeyPressed(sf::Keyboard::S) && !borderDown)
		{
			a.setPosition(sf::Vector2f(a.getPosition().x, a.getPosition().y + speed));
		}
		std::cout << a.getPosition().x << std::endl;
	}

	sf::Vector2f getPositionPlayer()
	{
		std::cout << a.getPosition().x << std::endl;
		return a.getPosition();
	}

};

class Controller
{
public:
	Controller(Player* player, Rect* rect)
	{
		this->player = *player;
		this->rect = *rect;
	}

	~Controller()
	{

	}

	void checkCollision()
	{
		/*if (player.getPositionPlayer().x + 20.f > rect.getPositionRect().x && player.getPositionPlayer().y+10.f< rect.getPositionRect().y+100.f
			&& player.getPositionPlayer().y + 10.f > rect.getPositionRect().y)
		{
			player.setBorderRight(true);
			std::cout << "Yes" << std::endl;
		}*/
		
		/*std::cout << player.getPositionPlayer().x << std::endl;
		std::cout << rect.getPositionRect().x << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;*/

		if (player.getPositionPlayer().x + 20.f > rect.getPositionRect().x)
		{
			std::cout << "First" << std::endl;
		
			if (player.getPositionPlayer().y + 10.f < rect.getPositionRect().y + 100.f)
			{
				std::cout << "Second" << std::endl;
				if (player.getPositionPlayer().y + 10.f > rect.getPositionRect().y)
				{
					std::cout << "Yes" << std::endl;
					player.setBorderRight(true);
				}
			}
				
		}

	}

private:
	Player player;
	Rect rect;
};

int main()
{
	sf::RenderWindow window(sf::VideoMode(300, 300), "Minecraft C++");
	Player* player = new Player();
	Rect* rect = new Rect();
	Controller control(player, rect);

	while (window.isOpen())
	{

		sf::Event event;
		while (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				window.close();
		}

		player->Move();
		control.checkCollision();
		window.clear();
		window.draw(player->getShape());
		window.draw(rect->getRect());
		window.display();
	}

	return 0;
}



