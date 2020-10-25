[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# A space where I can explore and learn about different Algorithms

I did not study computer science so this is kind of my weakness. So this is my playground for learning.

# Install

You will need conan (and therefore python) in order to run this out of the box. Afterwards its just the usual cmake call.

```
pip install conan
mkdir build && cd build
cmake ..
```

I changed the approach to have conan integrated into cmake so there is no hassle with the conan install command according to different profiles or selecting the right compiler. Since cmake has all the information this should make things way easier for everyone.

