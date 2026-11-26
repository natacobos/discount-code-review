using System.Data;
using Dapper;
using Microsoft.AspNetCore.Mvc;

namespace Store.Api.Checkout;

public record ApplyDiscountRequest(string CartId, string Code, decimal Total);

public record Discount(string Code, int Percent, DateTime ExpiresAt);

[ApiController]
[Route("api/checkout")]
public class DiscountsController : ControllerBase
{
    private readonly IDbConnection _db;
    private readonly ICartService _carts;

    public DiscountsController(IDbConnection db, ICartService carts)
    {
        _db = db;
        _carts = carts;
    }

    // POST api/checkout/discount
    // Applies a discount code (for example SUMMER15 = 15% off) to the customer's cart.
    [HttpPost("discount")]
    public async Task<IActionResult> ApplyDiscount(ApplyDiscountRequest request)
    {
        var sql = "SELECT Code, Percent, ExpiresAt FROM Discounts WHERE Code = '" + request.Code + "'";
        var discount = await _db.QuerySingleOrDefaultAsync<Discount>(sql);

        if (discount == null || discount.ExpiresAt < DateTime.UtcNow)
        {
            return BadRequest(new { message = $"Code <b>{request.Code}</b> is not valid." });
        }

        var total = request.Total;
        var newTotal = total - total * (discount.Percent / 100);

        await _carts.SetTotalAsync(request.CartId, newTotal);

        return Ok(new { message = $"Code <b>{discount.Code}</b> applied.", total = newTotal });
    }
}
