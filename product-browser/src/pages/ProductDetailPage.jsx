import { useState, useEffect } from "react";
import { Link, useParams } from "react-router";

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  useEffect(() => {
    async function loadProducts() {
      const res = await fetch(`https://dummyjson.com/products/${id}`);
      const data = await res.json();

      setProduct(data);
    }

    loadProducts();
  }, [id]);

  if (!product) return <p>Loading....</p>;

  return (
    <>
      <Link to="/">Back to Products</Link>
      <h2> {product.title}</h2>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
      <p>Category: {product.category}</p>
      <p>Rating:{product.rating}</p>
      <p>stock:{product.stock}</p>
    </>
  );
}
