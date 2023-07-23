# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .errors import LexerError
from .lexer import Lexer
from .logging import logger
from .token import Token

__version__ = "1.2"
__license__ = "Unlicense"
__author__ = "Leandro Benedet Garcia"
__author_email__ = "cerberus1746@gmail.com"
__description__ = "A generic pattern-based Lexer/tokenizer tool."
__url__ = "https://github.com/Cerberus1746/generic_lexer/"
__min_python_version__ = (3, 8)

__all__ = ["Lexer", "Token", "LexerError", "logger"]
