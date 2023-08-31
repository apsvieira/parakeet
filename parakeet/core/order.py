from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class OrderDim:
    dimension: str
    ascending: bool = True


@dataclass
class OrderBy:
    order_dims: List[OrderDim]

    @classmethod
    def from_dimensions(cls, dims: List[str], ascending: bool) -> "OrderBy":
        """Create an order by from a list of dimensions and a sort order.

        Parameters
        ----------
        dims : List[str]
            List of dimensions to order by.
        ascending : bool
            Sort order.

        Returns
        -------
        OrderBy
            List of dimensions and sort orders.

        """
        order_dims = [OrderDim(dim, ascending) for dim in dims]
        return cls(order_dims)

    @classmethod
    def from_str(cls, order_by: str) -> "OrderBy":
        """Parse an order by string into a list of dimensions and sort orders.

        Parameters
        ----------
        order_by : str
            Comma-separated list of dimensions to order by.
            Dimensions can be followed by " ASC" or " DESC" to specify the sort order.

        Returns
        -------
        OrderBy
            List of dimensions and sort orders.

        """
        order_dims = []
        for dim in order_by.split(","):
            # parse ASC and DESC from end of dimension
            dim = dim.strip()
            ascending = True
            if dim.upper().endswith(" ASC"):
                dim = dim[:-4]
            elif dim.upper().endswith(" DESC"):
                dim = dim[:-5]
                ascending = False
            order_dims.append(OrderDim(dim, ascending))

        return cls(order_dims)

    def to_pandas(self) -> Tuple[List[str], List[bool]]:
        """Convert the order by to a list of dimensions and sort orders."""
        return (
            [dim.dimension for dim in self.order_dims],
            [dim.ascending for dim in self.order_dims],
        )

    def to_bigquery(self) -> str:
        """Convert to an order by clause in BigQuery SQL."""
        dims = [
            f"{dim.dimension} ASC" if dim.ascending else f"{dim.dimension} DESC"
            for dim in self.order_dims
        ]
        return ", ".join(dims)
