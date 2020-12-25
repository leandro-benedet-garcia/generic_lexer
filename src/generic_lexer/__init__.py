# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import re
import sys


__version__ = "1.1.2"
__license__ = "MIT"
__author__ = "Leandro Benedet Garcia"
__author_email__ = "cerberus1746@gmail.com"
__description__ = "A generic pattern-based Lexer/tokenizer tool."
__url__ = "https://github.com/Cerberus1746/generic_lexer/"
__min_python_version__ = (3, 6, 1)


# +-------------------------------+
# | Python version specific stuff |
# +-------------------------------+
# Python versions under 3.7 doesn't have Pattern or Match, so we use str
# instead as a type
# Python version 3.9 implements support for [] in Pattern and Match
# but this does not work with other versions
# (Long live Tox/Nox)
if sys.version_info < (3, 7):
    MatchPattern = str
elif sys.version_info < (3, 9):
    MatchPattern = re.Match
else:
    MatchPattern = re.Match[str]

from .errors import LexerError
from .lexer import Lexer
from .logging import logger
from .token import Token

__all__ = ["Lexer", "Token", "LexerError", "logger"]
