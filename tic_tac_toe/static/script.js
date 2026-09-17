document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const statusEl = document.getElementById('status');
    const resetBtn = document.getElementById('resetBtn');
    let board = Array(9).fill(null);
    let currentPlayer = 'X';
    let gameOver = false;

    const winningCombos = [
        [0,1,2],[3,4,5],[6,7,8], // rows
        [0,3,6],[1,4,7],[2,5,8], // columns
        [0,4,8],[2,4,6] // diagonals
    ];

    function render() {
        board.forEach((mark, i) => {
            cells[i].textContent = mark ? mark : '';
        });
        if (gameOver) {
            // status already set
        } else {
            statusEl.textContent = `Player ${currentPlayer}'s turn`;
        }
    }

    function checkWinner() {
        for (const combo of winningCombos) {
            const [a,b,c] = combo;
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return board[a];
            }
        }
        return board.includes(null) ? null : 'Tie';
    }

    function handleClick(e) {
        const idx = parseInt(e.target.dataset.index);
        if (board[idx] || gameOver) return;
        board[idx] = currentPlayer;
        const winner = checkWinner();
        if (winner) {
            gameOver = true;
            if (winner === 'Tie') {
                statusEl.textContent = "It's a tie!";
            } else {
                statusEl.textContent = `Player ${winner} wins!`;
            }
        } else {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        }
        render();
    }

    function resetGame() {
        board = Array(9).fill(null);
        currentPlayer = 'X';
        gameOver = false;
        statusEl.textContent = '';
        render();
    }

    cells.forEach(cell => cell.addEventListener('click', handleClick));
    resetBtn.addEventListener('click', resetGame);
    render();
});
