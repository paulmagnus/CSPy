class Foo {
	public:
		Foo();
		Foo(int x);
		Foo(int x, float y);
	private:
		int x;
		float y;
};

Foo::Foo() {
	this->x = 0;
	this->y = 0;
}

Foo::Foo(int x, float y){
	this->x = x;
	this->y = y;
}

int main() {
	Foo bar0();
	Foo bar1(1, 1.0);
}