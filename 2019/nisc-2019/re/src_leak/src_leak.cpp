#include<iostream>
using namespace std;

typedef unsigned int uint;


template <bool Flag, class MaybeA, class MaybeB> class IfElse;

template <class MaybeA, class MaybeB>
class IfElse<true, MaybeA, MaybeB> {
public:
	using ResultType = MaybeA;
};

template <class MaybeA, class MaybeB>
class IfElse<false, MaybeA, MaybeB> {
public:
	using ResultType = MaybeB;
};


template <uint N, uint L, uint R> struct func1 {
	enum { mid = (L + R + 1) / 2 };

	using ResultType = typename IfElse<(N < mid * mid),
		func1<N, L, mid - 1>, func1<N, mid, R> >::ResultType;

	enum { result = ResultType::result };
};

template <uint N, uint L> struct func1<N, L, L> { enum { result = L }; };

template <uint N> struct _func1 { enum { result = func1<N, 1, N>::result }; };









template<size_t Input>
constexpr size_t func2 = (Input % 2) + func2< (Input / 2) >;

template<>
constexpr size_t func2<0> = 0;









template<size_t num>
constexpr size_t func3 = num % 2;









template<uint n, uint m>struct NEXTN {
	const static uint value = ((n % m != 0) * n);
};
template<uint n, uint m>struct NEXTM {
	const static uint value = (m * m <= n ? (m + 1) : 0);
};
template<uint n, uint m>struct TEST {
	const static uint value = TEST<NEXTN<n, m>::value, NEXTM<n, m>::value>::value;
};
template<uint m>struct TEST<0, m> {
	const static uint value = 0;
};
template<uint n>struct TEST<n, 0> {
	const static uint value = 1;
};
template<uint n>struct func4 {
	const static uint value = TEST<n, 2>::value;
};
template<>struct func4<1> {
	const static uint value = 0;
};
template<>struct func4<2> {
	const static uint value = 1;
};




int main(int argc, char**argv) {
	//input 5 uint numbers ,x1,x2,x3,x4,x5
	//the sum of them should be MIN


	cout << func3< func2<x1> > << endl;
	cout << func3< func2<x2> > << endl;
	cout << func3< func2<x3> > << endl;
	cout << func3< func2<x4> > << endl;
	cout << func3< func2<x5> > << endl;

	// output: 1 1 1 1 1


	cout << _func1<x1>::result << endl;
	cout << _func1<x2>::result << endl;
	cout << _func1<x3>::result << endl;
	cout << _func1<x4>::result << endl;
	cout << _func1<x5>::result << endl;

	//output: 963 4396 6666 1999 3141




	//how many "1" will func4<1>,func4<2>,fun4<3>......fun4<10000> ::value  return?
	x6 = count;


	// your flag is flag{x1-x2-x3-x4-x5-x6}
	// if x1=1,x2=2,x3=3,x4=4,x5=5,x6=6
	// flag is     flag{1-2-3-4-5-6}



	return 0;
}

