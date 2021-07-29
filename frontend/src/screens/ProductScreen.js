import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import { listProductDetails } from '../actions/productsActions'
import { useDispatch, useSelector } from 'react-redux'
import Rating from '../components/Rating'
import Loader from '../components/Loader'
import Message from '../components/Message'

function ProductScreen({ match, history }) {
    const [quantity, setQuantity] = useState(1)

    const dispatch = useDispatch()
    const productDetails = useSelector(state => state.productDetails)
    const { loading, error, product } = productDetails

    useEffect(() => {
        dispatch(listProductDetails(match.params.id))
    }, [dispatch, match])

    const addToCartHandler = () => {
        history.push(`/cart/${match.params.id}?qty=${quantity}`,)
    }

    return (
        <div>
            <Link to='/' className="btn btn-light my-3">Go Back</Link>
            { loading 
                ? <Loader/>
                : error
                    ? <Message variant="danger">{error}</Message>
                    : 
                    <Row>
                        <Col md={6}>
                            <Image src={ product.image } alt={product.name} fluid />
                        </Col>

                        <Col md={3}>
                            <ListGroup variant="flush">
                                <ListGroup.Item>
                                    <h3>{ product.name }</h3>
                                </ListGroup.Item>

                                <ListGroup.Item>
                                    <Rating value={product.rating} text={`${ product.numReviews } ratings`} color={'#f8e825'}/>
                                </ListGroup.Item>

                                <ListGroup.Item>
                                    Price: ${product.price}
                                </ListGroup.Item>
                                
                                <ListGroup.Item>
                                    Description: {product.description}
                                </ListGroup.Item>
                            </ListGroup>
                        </Col>

                        <Col md={3}>
                            <Card>
                                <ListGroup variant="flush">
                                    <ListGroup.Item>
                                        <Row>
                                            <Col>Price: </Col>
                                            <Col>
                                                <strong>${ product.price }</strong>
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>

                                    <ListGroup.Item>
                                        <Row>
                                            <Col>Status: </Col>
                                            <Col>
                                                <strong>{ product.count_in_stock > 0 ? 'In stock' : 'Out of stock' }</strong>
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>

                                    { product.count_in_stock > 0 && (
                                        <ListGroup.Item>
                                            <Row>
                                                <Col>Quantity</Col>
                                                <Col xs='auto' className='my-1'>
                                                    <Form.Control
                                                        as="select"
                                                        value={quantity}
                                                        onChange={(e) => setQuantity(e.target.value)}
                                                    >
                                                        {[...Array(product.count_in_stock).keys()].map((x) => (
                                                            <option key={x + 1} value={x + 1}>
                                                                {x + 1}
                                                            </option>
                                                        ))}
                                                    </Form.Control>
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    )}

                                    <Button 
                                    onClick={addToCartHandler}
                                    className="btn-block rounded" 
                                    disabled={ product.count_in_stock == 0 } 
                                    type='button'>
                                        Add to Cart
                                    </Button>
                                </ListGroup>
                            </Card>
                        </Col>
                    </Row>
            }       
            
        </div>
    )
}

export default ProductScreen
