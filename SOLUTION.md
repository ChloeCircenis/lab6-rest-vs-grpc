| Method          | Local | Same-Zone | Different Region |
|-----------------|-------|-----------|------------------|
| REST add        | 3.273 ms  | 3.700 ms |  349.586 ms   |
| gRPC add        |  0.751 ms | 1.415 ms |  166.553 ms   |
| REST rawimg     |  7.081 ms | 7.094 ms |  1498.326 ms  |
| gRPC rawimg     | 14.183 ms | 13.306 ms |   207.598 ms |
| REST dotproduct |  3.869 ms | 4.011 ms |   561.194 ms  |
| gRPC dotproduct |  0.820 ms | 1.537 ms |   165.402 ms  |
| REST jsonimg    | 24.548 ms | 23.630 ms |  1830.890 ms |
| gRPC jsonimg    | 21.775 ms | 19.652 ms |  195.983 ms  |
| PING            |  0.042 ms | 0.606 ms |  140.615 ms   |

Observations:
REST generally performs fastest locally, slightly slower in Same-Zone, and then much slower in Different Region. gRPC follows the same pattern, but is faster than REST in same-zone, except for with raw images, and is much faster than REST in different regions. We can see that the basic latency increases between local, same-zone, and different regions as well. So we can see that gRPC performs better across the three categories, while REST gets slower as it has to make repeated TCP connections, whereas gRPC uses the same one. 
